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
from analysis.behavior_analysis import steps_to_df, compute_behavior_metrics

# Optional: memory timeline helper (if implemented)
try:
    from analysis.memory_analysis import compute_memory_timeline
    HAS_MEMORY_TIMELINE = True
except ImportError:
    HAS_MEMORY_TIMELINE = False

# ----------------- BASIC PAGE CONFIG -----------------
st.set_page_config(
    page_title="GlassMind Navigator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- LOAD TRACES -----------------
traces = load_traces()
if not traces:
    st.error("❗ No traces found in `data/traces` yet. Run your agent to generate at least one trace.")
    st.stop()

# ----------------- SIDEBAR -----------------
st.sidebar.title("📁 Trace Explorer")

trace_names = [
    f"Trace {i+1} – {t.get('user_query', '')[:40]}..."
    for i, t in enumerate(traces)
]
choice = st.sidebar.selectbox(
    "Select a trace",
    options=list(range(len(traces))),
    format_func=lambda i: trace_names[i],
)

trace = traces[choice]
steps = trace["steps"]

st.sidebar.markdown("### 🧵 Steps")
st.sidebar.write(f"Total steps: **{len(steps)}**")

# Step selection for details tab
step_ids = [s["step_id"] for s in steps]
selected_step_id = st.sidebar.selectbox(
    "Focus step",
    options=step_ids,
    index=0,
)

# ----------------- HEADER -----------------
st.title("🧠 GlassMind Navigator – Investment Research Agent (Glass Box)")
st.caption(
    "Fully observable **investment research assistant** – every decision, tool call, "
    "and memory update is visible for debugging and trust."
)

# ----------------- TABS -----------------
tab_overview, tab_step, tab_behavior, tab_errors = st.tabs(
    ["📌 Overview & Timeline", "🔍 Step & Memory Detail", "📊 Behavior Patterns", "🐞 Error Replay"]
)

# ---------- TAB 1: OVERVIEW & TIMELINE ----------
with tab_overview:
    st.subheader("Overview")

    col_a, col_b = st.columns([2, 3])
    with col_a:
        st.markdown("**User query**")
        st.info(trace.get("user_query", ""))

    with col_b:
        st.markdown("**Final answer (truncated)**")
        st.write(trace.get("final_answer", "")[:600] + "…")

    st.markdown("---")
    st.subheader("Step Timeline")

    df_steps = pd.DataFrame(
        [
            {
                "Step": s["step_id"],
                "Node": s["node"],
                "Tool": s["tool"],
                "Thought": s["thought"],
            }
            for s in steps
        ]
    )

    st.dataframe(df_steps, width="stretch", height=350)

# ---------- TAB 2: STEP & MEMORY DETAIL ----------
with tab_step:
    st.subheader("Step & Memory Detail")

    # Map from id to step
    selected_step = next(s for s in steps if s["step_id"] == selected_step_id)

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        st.markdown(f"**Selected Step:** `{selected_step['step_id']}`")
        st.markdown(f"**Node:** `{selected_step['node']}`")
    with col_top2:
        st.markdown(f"**Tool:** `{selected_step['tool']}`" if selected_step["tool"] else "**Tool:** `None`")

    st.markdown("### 🧠 Thought at this step")
    st.write(selected_step["thought"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🗂 Memory Before")
        st.json(selected_step.get("memory_before", {}))
    with col2:
        st.markdown("### 📌 Memory After")
        st.json(selected_step.get("memory_after", {}))

    if selected_step["tool"]:
        st.markdown("### 🛠 Tool Call Details")
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            st.markdown("**Input**")
            st.json(selected_step.get("tool_input"))
        with tcol2:
            st.markdown("**Output**")
            st.json(selected_step.get("tool_output"))

    # Optional memory timeline diff (if you implemented it)
    if HAS_MEMORY_TIMELINE:
        try:
            st.markdown("### 🧬 Memory Change Summary (Timeline View)")
            timeline = compute_memory_timeline(trace)
            # If your compute_memory_timeline returns a list indexed by step-1:
            if isinstance(timeline, list) and len(timeline) >= selected_step_id:
                st.json(timeline[selected_step_id - 1])
            else:
                st.write("Memory timeline format not recognized.")
        except Exception as e:
            st.warning(f"Could not render memory timeline: {e}")

# ---------- TAB 3: BEHAVIOR PATTERNS ----------
with tab_behavior:
    st.subheader("Behavior Patterns (across all traces)")

    all_traces = traces  # already loaded
    df_all = steps_to_df(all_traces)
    metrics = compute_behavior_metrics(df_all)

    # Top metrics row
    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Total steps", metrics.get("total_steps", 0))
    mcol2.metric("Tool calls", str(metrics.get("tool_calls", 0)))
    mcol3.metric(
        "Tool usage rate",
        f"{metrics.get('tool_usage_rate', 0.0) * 100:.1f}%",
    )

    st.markdown("#### 🔧 Tool Usage")
    if df_all["tool"].notna().any():
        st.bar_chart(df_all["tool"].value_counts(dropna=True))
    else:
        st.write("No tool calls recorded yet.")

    st.markdown("#### 🔁 Node Frequency")
    st.bar_chart(df_all["node"].value_counts())

    st.markdown("#### Raw Metrics JSON")
    st.json(metrics)

# ---------- TAB 4: ERROR REPLAY ----------
with tab_errors:
    st.subheader("Error Replay Mode")

    # Simple heuristic: any step with 'error' in thought or tool_output
    failed_steps = []
    for s in steps:
        thought_text = (s.get("thought") or "").lower()
        tool_out_text = str(s.get("tool_output") or "").lower()
        if "error" in thought_text or "error" in tool_out_text:
            failed_steps.append(s)

    if failed_steps:
        st.write(f"Detected **{len(failed_steps)}** potential failure points.")
        for fs in failed_steps:
            with st.expander(f"❌ Step {fs['step_id']} – Node `{fs['node']}`"):
                st.markdown("**Thought**")
                st.write(fs["thought"])
                st.markdown("**Memory Before**")
                st.json(fs.get("memory_before", {}))
                st.markdown("**Memory After**")
                st.json(fs.get("memory_after", {}))
                if fs.get("tool"):
                    st.markdown("**Tool Output**")
                    st.json(fs.get("tool_output"))
    else:
        st.success("✅ No obvious failure points detected in this trace.")

# ----------------- DISCLAIMER -----------------
st.markdown(
    "---\n"
    "> ⚠️ **Disclaimer:** This system is an *educational investment research assistant*. "
    "It does **not** provide financial advice. Always do your own research and consult a "
    "qualified professional before making investment decisions."
)
