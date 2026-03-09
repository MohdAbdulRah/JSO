"""
rag_engine.py – RAG Pipeline Orchestrator for JSO Career Intelligence
Coordinates all agents in the multi-agent workflow:
  Resume → Profile → Embeddings → Vector Search → Matching → Skill Gap → Reasoning
"""

from jobs_dataset import get_jobs
from memory import set_memory, log_agent
from agents import (
    ResumeIntelligenceAgent,
    EmbeddingGeneratorAgent,
    JobMatchingAgent,
    SkillGapAnalysisAgent,
    GeminiReasoningAgent,
)
import vector_store


def _build_jobs_lookup(jobs: list[dict]) -> dict:
    return {job["id"]: job for job in jobs}


def run_pipeline(uploaded_file) -> dict:
    """Execute the full multi-agent RAG pipeline.

    Parameters
    ----------
    uploaded_file : BytesIO-like
        The uploaded resume PDF file object.

    Returns
    -------
    dict with keys:
        candidate_profile, recommended_jobs, skill_gaps, learning_paths, explanations
    """
    results = {
        "candidate_profile": {},
        "recommended_jobs": [],
        "skill_gaps": {},
        "explanations": [],
        "pipeline_status": [],
    }

    # ── Step 1: Resume Intelligence Agent ──────────────────────────
    log_agent("Pipeline", "running", "Step 1/6 – Parsing resume…")
    results["pipeline_status"].append(("Resume Intelligence Agent", "running"))

    resume_text = ResumeIntelligenceAgent.extract_text_from_pdf(uploaded_file)
    if not resume_text.strip():
        results["pipeline_status"][-1] = ("Resume Intelligence Agent", "error")
        raise ValueError("Could not extract text from the uploaded PDF. Please upload a text-based PDF resume.")

    candidate_profile = ResumeIntelligenceAgent.analyse(resume_text)
    results["candidate_profile"] = candidate_profile
    set_memory("candidate_profile", candidate_profile)
    results["pipeline_status"][-1] = ("Resume Intelligence Agent", "done")

    # ── Step 2: Embedding Generator Agent ──────────────────────────
    log_agent("Pipeline", "running", "Step 2/6 – Indexing jobs…")
    results["pipeline_status"].append(("Embedding Generator Agent", "running"))

    jobs = get_jobs()
    jobs_lookup = _build_jobs_lookup(jobs)
    EmbeddingGeneratorAgent.index_jobs(jobs)
    results["pipeline_status"][-1] = ("Embedding Generator Agent", "done")

    # ── Step 3: RAG – Vector Search ────────────────────────────────
    log_agent("Pipeline", "running", "Step 3/6 – Semantic search in ChromaDB…")
    results["pipeline_status"].append(("RAG Vector Search", "running"))

    candidate_query = EmbeddingGeneratorAgent.create_candidate_query(candidate_profile)
    search_results = vector_store.search_jobs(candidate_query, n_results=5)
    results["pipeline_status"][-1] = ("RAG Vector Search", "done")

    # ── Step 4: Job Matching Agent ─────────────────────────────────
    log_agent("Pipeline", "running", "Step 4/6 – Ranking matches…")
    results["pipeline_status"].append(("Job Matching Agent", "running"))

    ranked_jobs = JobMatchingAgent.rank(search_results, jobs_lookup)
    results["recommended_jobs"] = ranked_jobs
    set_memory("recommended_jobs", ranked_jobs)
    results["pipeline_status"][-1] = ("Job Matching Agent", "done")

    # ── Step 5: Skill Gap Analysis Agent ───────────────────────────
    log_agent("Pipeline", "running", "Step 5/6 – Analysing skill gaps…")
    results["pipeline_status"].append(("Skill Gap Analysis Agent", "running"))

    candidate_skills = candidate_profile.get("skills", [])
    skill_gaps = SkillGapAnalysisAgent.analyse(candidate_skills, ranked_jobs)
    results["skill_gaps"] = skill_gaps
    set_memory("skill_gaps", skill_gaps.get("missing_skills", []))
    set_memory("learning_paths", skill_gaps.get("learning_paths", []))
    results["pipeline_status"][-1] = ("Skill Gap Analysis Agent", "done")

    # ── Step 6: Gemini Reasoning Agent ─────────────────────────────
    log_agent("Pipeline", "running", "Step 6/6 – Generating AI explanations…")
    results["pipeline_status"].append(("Gemini Reasoning Agent", "running"))

    explanations = GeminiReasoningAgent.explain_batch(candidate_profile, ranked_jobs)
    results["explanations"] = explanations
    results["pipeline_status"][-1] = ("Gemini Reasoning Agent", "done")

    log_agent("Pipeline", "done", "All agents completed successfully.")
    return results
