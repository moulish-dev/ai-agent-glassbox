# frontend/run_agent_page.py

import os
import sys
import streamlit as st
from datetime import datetime

# --- Ensure project root is importable ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph import run_agent
from analysis.traces_loader import save_trace


st.set_page_config(page_title="Run New Trace", layout="wide")

st.title("🧠 Run New Agent Trace")
st.caption("Enter any query — the agent will run and produce a full transparent trajectory.")

# --- Input box ---
user_query = st.text_input(
    "Type your question or research query",
    placeholder="e.g., 'Is Nvidia stock a good buy?', 'Explain Bitcoin's long-term outlook', etc."
)

# --- Run button ---
if st.button("🚀 Run Agent"):
    if not user_query.strip():
        st.error("Please enter a query before running the agent.")
        st.stop()

    with st.spinner("Agent thinking... generating trace..."):
        # Run the agent
        state = run_agent(user_query)

        # Save trace
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name = f"trace_{timestamp}"
        save_trace(state, trace_name)

    st.success(f"Trace generated successfully: **{trace_name}.json**")
    st.info("Go to **GlassMind Navigator** page to view this trace.")
