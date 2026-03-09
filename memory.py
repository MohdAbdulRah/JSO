"""
memory.py – Agent Memory System for JSO Career Intelligence
Uses Streamlit session_state for short-term memory, simulating persistent
agent behaviour across interactions within a single session.
"""

import streamlit as st


def _ensure_memory():
    """Initialise memory structure in session_state if not present."""
    if "agent_memory" not in st.session_state:
        st.session_state.agent_memory = {
            "candidate_profile": {},
            "recommended_jobs": [],
            "skill_gaps": [],
            "learning_paths": [],
            "interaction_history": [],
            "agent_logs": [],
        }


def get_memory(key: str = None):
    """Return full memory dict or a specific key."""
    _ensure_memory()
    if key:
        return st.session_state.agent_memory.get(key)
    return st.session_state.agent_memory


def set_memory(key: str, value):
    """Set a specific memory key."""
    _ensure_memory()
    st.session_state.agent_memory[key] = value


def append_memory(key: str, value):
    """Append a value to a list-type memory key."""
    _ensure_memory()
    if isinstance(st.session_state.agent_memory.get(key), list):
        st.session_state.agent_memory[key].append(value)


def log_agent(agent_name: str, status: str, detail: str = ""):
    """Add an entry to the agent activity log."""
    _ensure_memory()
    st.session_state.agent_memory["agent_logs"].append(
        {"agent": agent_name, "status": status, "detail": detail}
    )


def clear_memory():
    """Reset all memory."""
    if "agent_memory" in st.session_state:
        del st.session_state.agent_memory
    _ensure_memory()
