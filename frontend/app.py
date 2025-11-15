import os
import sys

# Ensure project root is on sys.path so we can import `analysis` and `backend`
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd
from analysis.traces_loader import load_traces

st.set_page_config(page_title="GlassMind Navigator", layout="wide")

st.title("GlassMind Navigator – Agent Trajectory Explorer")

traces = load_traces()
if not traces:
    st.warning("No traces found in data/traces yet.")
    st.stop()

trace_names = [f"Trace {i+1}" for i in range(len(traces))]
choice = st.selectbox("Select a trace", options=list(range(len(traces))), format_func=lambda i: trace_names[i])

trace = traces[choice]
steps = trace["steps"]

# Show basic info
st.subheader("Overview")
st.write(f"User query: `{trace['user_query']}`")
st.write(f"Final answer (first 200 chars): {trace.get('final_answer', '')[:200]}…")

# Steps table
st.subheader("Step Timeline")
df = pd.DataFrame([
    {
        "step_id": s["step_id"],
        "node": s["node"],
        "tool": s["tool"],
        "thought": s["thought"],
    }
    for s in steps
])
st.dataframe(df, width="stretch")

# Memory timeline – show diff-ish view
st.subheader("Memory Timeline")

selected_step_idx = st.slider("Select step", min_value=1, max_value=len(steps), value=1)
selected_step = steps[selected_step_idx - 1]

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Memory Before**")
    st.json(selected_step["memory_before"])
with col2:
    st.markdown("**Memory After**")
    st.json(selected_step["memory_after"])

st.markdown("**Thought at this step**")
st.write(selected_step["thought"])
if selected_step["tool"]:
    st.markdown("**Tool Call**")
    st.write(f"Tool: `{selected_step['tool']}`")
    st.write("Input:")
    st.json(selected_step.get("tool_input"))
    st.write("Output:")
    st.json(selected_step.get("tool_output"))


from analysis.behavior_analysis import steps_to_df, compute_behavior_metrics

all_traces = load_traces()
df_all = steps_to_df(all_traces)
metrics = compute_behavior_metrics(df_all)

st.subheader("Behavior Patterns (across all traces)")
st.write(metrics)

st.bar_chart(df_all["node"].value_counts())
if df_all["tool"].notna().any():
    st.bar_chart(df_all["tool"].value_counts(dropna=True))


from analysis.memory_analysis import compute_memory_changes_for_trace

memory_diffs = compute_memory_changes_for_trace(trace)
current_diff = memory_diffs[selected_step_idx - 1]["diff"]
st.subheader("Memory Diff at this step")
st.json(current_diff)
