"""
agents.py – Multi-Agent Definitions for JSO Career Intelligence System
Each agent is a class encapsulating a distinct responsibility.
Gemini calls go through a shared helper `call_gemini`.
"""

import json
import os
import re
from io import BytesIO

from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

import vector_store
from memory import log_agent

# ---------------------------------------------------------------------------
# Gemini configuration
# ---------------------------------------------------------------------------
load_dotenv()

_gemini_configured = False


def _ensure_gemini():
    global _gemini_configured
    if not _gemini_configured:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY not found. Please set it in a .env file or as an environment variable."
            )
        genai.configure(api_key=api_key)
        _gemini_configured = True


def call_gemini(prompt: str, temperature: float = 0.4) -> str:
    """Call Gemini and return the text response."""
    _ensure_gemini()
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=temperature),
    )
    return response.text


# ╔══════════════════════════════════════════════════════════════╗
# ║  1. Resume Intelligence Agent                               ║
# ╚══════════════════════════════════════════════════════════════╝

class ResumeIntelligenceAgent:
    """Parse a PDF resume and extract a structured candidate profile."""

    NAME = "Resume Intelligence Agent"

    @staticmethod
    def extract_text_from_pdf(file: BytesIO) -> str:
        """Extract text from a PDF file using pypdf (pyParser)."""
        reader = PdfReader(file)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)

    @staticmethod
    def analyse(resume_text: str) -> dict:
        """Use Gemini to extract structured profile from resume text."""
        log_agent(ResumeIntelligenceAgent.NAME, "running", "Analysing resume with Gemini…")

        prompt = f"""You are an expert career analyst AI.

Analyse the following resume text and return ONLY a valid JSON object (no markdown, no backticks) with these keys:
- "name": candidate name (string)
- "skills": list of technical and soft skills (list of strings, max 15)
- "experience_level": one of "Junior", "Mid-Level", or "Senior"
- "years_of_experience": estimated total years (integer)
- "preferred_domain": primary career domain (string)
- "education": highest qualification (string)
- "summary": a 2-3 sentence professional summary (string)

Resume Text:
\"\"\"
{resume_text[:4000]}
\"\"\"
"""
        raw = call_gemini(prompt, temperature=0.2)
        # Strip any markdown fences Gemini might add
        raw = raw.strip()
        raw = re.sub(r"^```(?:json)?", "", raw)
        raw = re.sub(r"```$", "", raw)
        raw = raw.strip()

        try:
            profile = json.loads(raw)
        except json.JSONDecodeError:
            profile = {
                "name": "Unknown",
                "skills": [],
                "experience_level": "Unknown",
                "years_of_experience": 0,
                "preferred_domain": "Unknown",
                "education": "Unknown",
                "summary": raw[:300],
            }

        log_agent(ResumeIntelligenceAgent.NAME, "done", f"Extracted {len(profile.get('skills', []))} skills")
        return profile


# ╔══════════════════════════════════════════════════════════════╗
# ║  2. Embedding Generator Agent                               ║
# ╚══════════════════════════════════════════════════════════════╝

class EmbeddingGeneratorAgent:
    """Generates embeddings for candidates and jobs via vector_store."""

    NAME = "Embedding Generator Agent"

    @staticmethod
    def index_jobs(jobs: list[dict]) -> int:
        log_agent(EmbeddingGeneratorAgent.NAME, "running", "Indexing job dataset into ChromaDB…")
        count = vector_store.index_jobs(jobs)
        log_agent(EmbeddingGeneratorAgent.NAME, "done", f"Indexed {count} jobs")
        return count

    @staticmethod
    def create_candidate_query(profile: dict) -> str:
        """Build a natural-language query from the candidate profile for vector search."""
        skills = ", ".join(profile.get("skills", []))
        domain = profile.get("preferred_domain", "")
        level = profile.get("experience_level", "")
        summary = profile.get("summary", "")
        return (
            f"Candidate skilled in {skills}. "
            f"Experience level: {level}. "
            f"Preferred domain: {domain}. "
            f"{summary}"
        )


# ╔══════════════════════════════════════════════════════════════╗
# ║  3. Job Matching Intelligence Agent                          ║
# ╚══════════════════════════════════════════════════════════════╝

class JobMatchingAgent:
    """Score and rank job matches from RAG retrieval results."""

    NAME = "Job Matching Agent"

    @staticmethod
    def rank(search_results: dict, jobs_lookup: dict) -> list[dict]:
        """Convert ChromaDB distances into match scores and return ranked list.

        search_results: output of vector_store.search_jobs()
        jobs_lookup: dict keyed by job id for full job data
        """
        log_agent(JobMatchingAgent.NAME, "running", "Computing match scores…")

        ranked = []
        ids = search_results["ids"][0]
        distances = search_results["distances"][0]
        metadatas = search_results["metadatas"][0]

        for job_id, distance, meta in zip(ids, distances, metadatas):
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            # Convert to a 0-100% score
            score = max(0, round((1 - distance / 2) * 100, 1))
            job_data = jobs_lookup.get(job_id, {})
            ranked.append({
                "id": job_id,
                "title": meta.get("title", "Unknown"),
                "company": meta.get("company", "N/A"),
                "industry": meta.get("industry", "N/A"),
                "experience_level": meta.get("experience_level", "N/A"),
                "required_skills": [s.strip() for s in meta.get("required_skills", "").split(",")],
                "description": job_data.get("description", ""),
                "match_score": score,
            })

        ranked.sort(key=lambda x: x["match_score"], reverse=True)
        log_agent(JobMatchingAgent.NAME, "done", f"Ranked {len(ranked)} jobs")
        return ranked


# ╔══════════════════════════════════════════════════════════════╗
# ║  4. Skill Gap Analysis Agent                                 ║
# ╚══════════════════════════════════════════════════════════════╝

class SkillGapAnalysisAgent:
    """Compare candidate skills with job requirements to find gaps."""

    NAME = "Skill Gap Analysis Agent"

    @staticmethod
    def analyse(candidate_skills: list[str], top_jobs: list[dict]) -> dict:
        """Return missing skills and learning recommendations."""
        log_agent(SkillGapAnalysisAgent.NAME, "running", "Identifying skill gaps…")

        candidate_set = {s.lower().strip() for s in candidate_skills}
        all_required: dict[str, int] = {}  # skill → frequency across top jobs

        for job in top_jobs:
            for skill in job.get("required_skills", []):
                sl = skill.strip()
                if sl.lower() not in candidate_set and sl:
                    all_required[sl] = all_required.get(sl, 0) + 1

        # Sort by frequency (most demanded first)
        missing = sorted(all_required.items(), key=lambda x: x[1], reverse=True)
        missing_skills = [s for s, _ in missing[:10]]

        # Use Gemini to suggest learning resources
        learning = []
        if missing_skills:
            prompt = f"""You are a career development advisor.
Given these missing skills that a candidate needs to learn:
{', '.join(missing_skills)}

Suggest a brief learning path: for each skill, provide ONE recommended course or resource name.
Return ONLY a valid JSON list of objects with keys "skill" and "resource". No markdown, no backticks.
Example: [{{"skill": "Docker", "resource": "Docker Mastery on Udemy"}}]"""

            raw = call_gemini(prompt, temperature=0.3)
            raw = raw.strip()
            raw = re.sub(r"^```(?:json)?", "", raw)
            raw = re.sub(r"```$", "", raw)
            raw = raw.strip()
            try:
                learning = json.loads(raw)
            except json.JSONDecodeError:
                learning = [{"skill": s, "resource": "Search online courses"} for s in missing_skills]

        log_agent(SkillGapAnalysisAgent.NAME, "done", f"Found {len(missing_skills)} skill gaps")
        return {"missing_skills": missing_skills, "learning_paths": learning}


# ╔══════════════════════════════════════════════════════════════╗
# ║  5. Gemini Reasoning Agent                                   ║
# ╚══════════════════════════════════════════════════════════════╝

class GeminiReasoningAgent:
    """Generate natural-language explanations for job recommendations."""

    NAME = "Gemini Reasoning Agent"

    @staticmethod
    def explain(candidate_profile: dict, job: dict) -> str:
        """Return a concise explanation for why this job is a good match."""
        log_agent(GeminiReasoningAgent.NAME, "running", f"Explaining match for {job.get('title')}…")

        skills = ", ".join(candidate_profile.get("skills", []))
        prompt = f"""You are an AI career advisor providing explainable recommendations.

Candidate skills: {skills}
Candidate experience level: {candidate_profile.get('experience_level', 'N/A')}
Candidate preferred domain: {candidate_profile.get('preferred_domain', 'N/A')}

Job Title: {job.get('title')}
Required Skills: {', '.join(job.get('required_skills', []))}
Job Description: {job.get('description', '')}
Match Score: {job.get('match_score', 0)}%

In 2-3 sentences, explain why this job is recommended for this candidate. Be specific about skill alignment and growth opportunities."""

        explanation = call_gemini(prompt, temperature=0.5)
        log_agent(GeminiReasoningAgent.NAME, "done", f"Explained {job.get('title')}")
        return explanation.strip()

    @staticmethod
    def explain_batch(candidate_profile: dict, jobs: list[dict]) -> list[str]:
        """Generate explanations for a list of jobs."""
        explanations = []
        for job in jobs:
            try:
                exp = GeminiReasoningAgent.explain(candidate_profile, job)
            except Exception as e:
                exp = f"Explanation unavailable: {e}"
            explanations.append(exp)
        return explanations
