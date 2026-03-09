"""
app.py – Streamlit Dashboard for JSO Agentic Career Intelligence System
Run with:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from memory import get_memory, clear_memory
from rag_engine import run_pipeline

# ───────────────────────────────────────────────────────────────
# Page Config
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JSO – AI Career Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────────────────────────────────────────
# Custom CSS – Modern Dark AI SaaS Theme
# ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }

    /* ── Sidebar ────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0ff;
    }

    /* ── Cards ──────────────────────────────────────── */
    .card {
        background: linear-gradient(135deg, #1e1e3f 0%, #2a2a5a 100%);
        border: 1px solid rgba(120, 120, 255, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(80,80,255,0.15);
    }
    .card h3 { color: #a0a0ff; margin: 0 0 0.5rem 0; }
    .card p  { color: #c8c8e8; margin: 0.25rem 0; }

    /* ── Skill Tags ─────────────────────────────────── */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.15rem;
        letter-spacing: 0.02em;
    }
    .skill-tag.missing {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
    }

    /* ── Score Badge ────────────────────────────────── */
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: #fff;
        padding: 0.3rem 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* ── Agent Status ───────────────────────────────── */
    .agent-status {
        display: flex;
        align-items: center;
        padding: 0.4rem 0;
        font-size: 0.85rem;
        color: #c8c8e8;
    }
    .agent-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        margin-right: 0.5rem;
        flex-shrink: 0;
    }
    .dot-done    { background: #10b981; box-shadow: 0 0 6px #10b981; }
    .dot-running { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
    .dot-error   { background: #ef4444; box-shadow: 0 0 6px #ef4444; }
    .dot-pending { background: #6b7280; }

    /* ── Header Banner ──────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(165,160,255,0.1);
    }
    .hero h1 { color: #e0e0ff; font-size: 2rem; margin-bottom: 0.25rem; }
    .hero p  { color: #a5b4fc; font-size: 1rem; margin: 0; }

    /* ── Metric Boxes ───────────────────────────────── */
    .metric-box {
        background: linear-gradient(135deg, #1e1e3f, #2a2a5a);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid rgba(120,120,255,0.12);
    }
    .metric-box .value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-box .label { color: #9ca3af; font-size: 0.85rem; margin-top: 0.25rem; }

    /* ── Hide Streamlit clutter ─────────────────────── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────
# Helper renderers
# ───────────────────────────────────────────────────────────────
def render_skill_tags(skills: list, css_class: str = "skill-tag") -> str:
    return " ".join(f'<span class="{css_class}">{s}</span>' for s in skills)


def render_agent_status(statuses: list[tuple[str, str]]) -> str:
    html = ""
    for name, status in statuses:
        dot_class = {"done": "dot-done", "running": "dot-running", "error": "dot-error"}.get(status, "dot-pending")
        icon = {"done": "✅", "running": "⏳", "error": "❌"}.get(status, "⬜")
        html += f'<div class="agent-status"><span class="agent-dot {dot_class}"></span>{icon} {name}</div>'
    return html


# ───────────────────────────────────────────────────────────────
# SIDEBAR
# ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 JSO Career Intelligence")
    st.markdown("**Agentic AI · RAG · Gemini**")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume (PDF)",
        type=["pdf"],
        help="Upload a text-based PDF resume. Scanned images are not supported.",
    )

    analyse_btn = st.button("🚀 Analyse Resume", use_container_width=True, type="primary")

    st.markdown("---")
    st.markdown("### 🔄 Agent Workflow")

    # Show agent pipeline statuses
    if "pipeline_results" in st.session_state and st.session_state.pipeline_results:
        statuses = st.session_state.pipeline_results.get("pipeline_status", [])
        st.markdown(render_agent_status(statuses), unsafe_allow_html=True)
    else:
        default_agents = [
            ("Resume Intelligence Agent", "pending"),
            ("Embedding Generator Agent", "pending"),
            ("RAG Vector Search", "pending"),
            ("Job Matching Agent", "pending"),
            ("Skill Gap Analysis Agent", "pending"),
            ("Gemini Reasoning Agent", "pending"),
        ]
        st.markdown(render_agent_status(default_agents), unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Reset Session", use_container_width=True):
        clear_memory()
        if "pipeline_results" in st.session_state:
            del st.session_state.pipeline_results
        st.rerun()

    st.markdown("---")
    st.caption("JSO Phase-2 · Agentic Career Intelligence · v0.1")


# ───────────────────────────────────────────────────────────────
# Run Pipeline
# ───────────────────────────────────────────────────────────────
if analyse_btn and uploaded_file is not None:
    with st.spinner("🤖 Running multi-agent pipeline… This may take a minute."):
        try:
            results = run_pipeline(uploaded_file)
            st.session_state.pipeline_results = results
        except Exception as e:
            st.error(f"❌ Pipeline error: {e}")
            st.stop()

elif analyse_btn and uploaded_file is None:
    st.warning("⚠️ Please upload a resume PDF first.")

# ───────────────────────────────────────────────────────────────
# MAIN DASHBOARD
# ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧠 Agentic Career Intelligence</h1>
    <p>AI-powered job matching · Multi-agent RAG architecture · Gemini reasoning</p>
</div>
""", unsafe_allow_html=True)

if "pipeline_results" not in st.session_state or not st.session_state.pipeline_results:
    # Landing state
    st.markdown("""
    <div class="card" style="text-align:center; padding: 3rem 2rem;">
        <h3 style="font-size:1.5rem; color:#818cf8;">Welcome to JSO Career Intelligence</h3>
        <p style="font-size:1.05rem; max-width:600px; margin:1rem auto;">
            Upload your resume in the sidebar to activate the multi-agent AI pipeline.
            Our system will extract your skills, find the best job matches, and provide
            personalised career intelligence — all powered by Gemini and RAG.
        </p>
        <p style="color:#6366f1; font-size:0.9rem; margin-top:1.5rem;">
            📄 Upload Resume → 🤖 AI Analysis → 🎯 Smart Matches → 📊 Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Unpack results ──
results = st.session_state.pipeline_results
profile = results["candidate_profile"]
jobs = results["recommended_jobs"]
skill_gaps = results["skill_gaps"]
explanations = results["explanations"]

# ───────────────────────────────────────────────────────────────
# Metric Row
# ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="value">{len(profile.get('skills', []))}</div>
        <div class="label">Skills Detected</div>
    </div>""", unsafe_allow_html=True)
with c2:
    top_score = jobs[0]["match_score"] if jobs else 0
    st.markdown(f"""
    <div class="metric-box">
        <div class="value">{top_score}%</div>
        <div class="label">Top Match Score</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="value">{len(jobs)}</div>
        <div class="label">Jobs Matched</div>
    </div>""", unsafe_allow_html=True)
with c4:
    gap_count = len(skill_gaps.get("missing_skills", []))
    st.markdown(f"""
    <div class="metric-box">
        <div class="value">{gap_count}</div>
        <div class="label">Skill Gaps</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ───────────────────────────────────────────────────────────────
# Row 1: Candidate Profile + Top Match
# ───────────────────────────────────────────────────────────────
col_profile, col_top = st.columns([1, 1])

with col_profile:
    st.markdown("### 👤 Candidate Profile")
    skills_html = render_skill_tags(profile.get("skills", []))
    st.markdown(f"""
    <div class="card">
        <h3>{profile.get('name', 'Candidate')}</h3>
        <p><strong>Experience:</strong> {profile.get('experience_level', 'N/A')} · {profile.get('years_of_experience', '?')} years</p>
        <p><strong>Domain:</strong> {profile.get('preferred_domain', 'N/A')}</p>
        <p><strong>Education:</strong> {profile.get('education', 'N/A')}</p>
        <p style="margin-top:0.75rem;"><strong>Skills:</strong></p>
        <div style="margin-top:0.35rem;">{skills_html}</div>
        <p style="margin-top:1rem; color:#9ca3af; font-style:italic;">{profile.get('summary', '')}</p>
    </div>
    """, unsafe_allow_html=True)

with col_top:
    if jobs:
        best = jobs[0]
        st.markdown("### 🏆 Top Recommended Job")
        st.markdown(f"""
        <div class="card" style="border-color: rgba(16,185,129,0.3);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0;">{best['title']}</h3>
                <span class="score-badge">{best['match_score']}%</span>
            </div>
            <p style="color:#818cf8;">{best.get('company', '')} · {best['industry']}</p>
            <p>{best.get('description', '')}</p>
            <p style="margin-top:0.5rem;"><strong>Required:</strong></p>
            <div>{render_skill_tags(best.get('required_skills', []))}</div>
        </div>
        """, unsafe_allow_html=True)
        if explanations:
            with st.expander("🤖 AI Explanation", expanded=True):
                st.info(explanations[0])

# ───────────────────────────────────────────────────────────────
# Row 2: All Job Recommendations
# ───────────────────────────────────────────────────────────────
st.markdown("### 🎯 Job Recommendations")

for idx, job in enumerate(jobs):
    with st.container():
        jc1, jc2 = st.columns([3, 1])
        with jc1:
            req_skills_html = render_skill_tags(job.get("required_skills", []))
            st.markdown(f"""
            <div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="margin:0;">{job['title']}</h3>
                    <span class="score-badge">{job['match_score']}%</span>
                </div>
                <p style="color:#818cf8;">{job.get('company', '')} · {job['industry']} · {job['experience_level']}</p>
                <p>{job.get('description', '')}</p>
                <div style="margin-top:0.5rem;">{req_skills_html}</div>
            </div>
            """, unsafe_allow_html=True)
        with jc2:
            # Match score radial gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=job["match_score"],
                number={"suffix": "%", "font": {"color": "#e0e0ff", "size": 28}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#4b5563", "dtick": 25},
                    "bar": {"color": "#6366f1"},
                    "bgcolor": "#1e1e3f",
                    "bordercolor": "rgba(120,120,255,0.2)",
                    "steps": [
                        {"range": [0, 50], "color": "rgba(239,68,68,0.15)"},
                        {"range": [50, 75], "color": "rgba(245,158,11,0.15)"},
                        {"range": [75, 100], "color": "rgba(16,185,129,0.15)"},
                    ],
                },
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=160, margin=dict(t=30, b=10, l=30, r=30),
                font={"color": "#c8c8e8"},
            )
            st.plotly_chart(fig, use_container_width=True, key=f"gauge_{idx}")

        if idx < len(explanations):
            with st.expander(f"🤖 Why this match?", expanded=False):
                st.info(explanations[idx])

# ───────────────────────────────────────────────────────────────
# Row 3: Skill Gap + Analytics
# ───────────────────────────────────────────────────────────────
st.markdown("---")
gap_col, analytics_col = st.columns([1, 1])

with gap_col:
    st.markdown("### 🔍 Skill Gap Analysis")
    missing = skill_gaps.get("missing_skills", [])
    learning = skill_gaps.get("learning_paths", [])

    if missing:
        missing_html = render_skill_tags(missing, "skill-tag missing")
        st.markdown(f"""
        <div class="card">
            <h3>Missing Skills</h3>
            <div>{missing_html}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📚 Recommended Learning Paths")
        for item in learning:
            if isinstance(item, dict):
                st.markdown(f"- **{item.get('skill', '')}**: {item.get('resource', '')}")
            else:
                st.markdown(f"- {item}")
    else:
        st.success("🎉 No significant skill gaps detected! You're a great match.")

with analytics_col:
    st.markdown("### 📊 Analytics")

    # Match Score Bar Chart
    if jobs:
        df_scores = pd.DataFrame([
            {"Job": j["title"][:25], "Match Score": j["match_score"]}
            for j in jobs
        ])
        fig_bar = px.bar(
            df_scores, x="Match Score", y="Job", orientation="h",
            color="Match Score",
            color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
            range_color=[0, 100],
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250, margin=dict(t=10, b=10, l=10, r=10),
            font={"color": "#c8c8e8"},
            showlegend=False,
            xaxis={"gridcolor": "rgba(120,120,255,0.08)", "range": [0, 100]},
            yaxis={"gridcolor": "rgba(0,0,0,0)"},
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="bar_scores")

    # Skill Distribution (candidate skills frequency across matched jobs)
    if profile.get("skills"):
        skill_freq: dict[str, int] = {}
        for s in profile["skills"]:
            for j in jobs:
                if s.lower() in [rs.lower() for rs in j.get("required_skills", [])]:
                    skill_freq[s] = skill_freq.get(s, 0) + 1

        if skill_freq:
            df_skills = pd.DataFrame(
                [{"Skill": k, "Demand": v} for k, v in sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)]
            )
            fig_skill = px.bar(
                df_skills, x="Demand", y="Skill", orientation="h",
                color="Demand",
                color_continuous_scale=["#6366f1", "#c084fc"],
            )
            fig_skill.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=220, margin=dict(t=10, b=10, l=10, r=10),
                font={"color": "#c8c8e8"},
                showlegend=False,
                xaxis={"gridcolor": "rgba(120,120,255,0.08)", "dtick": 1},
                yaxis={"gridcolor": "rgba(0,0,0,0)"},
                coloraxis_showscale=False,
            )
            st.markdown("#### Skill Demand Across Top Matches")
            st.plotly_chart(fig_skill, use_container_width=True, key="skill_dist")

# ───────────────────────────────────────────────────────────────
# Footer
# ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6b7280; font-size:0.8rem; padding:1rem 0;">
    <strong>JSO Agentic Career Intelligence System</strong> · Phase-2 Prototype<br>
    Powered by Gemini · ChromaDB · SentenceTransformers · Multi-Agent RAG Architecture
</div>
""", unsafe_allow_html=True)
