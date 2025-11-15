import pandas as pd
from typing import List, Dict, Any

def steps_to_df(traces: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for tidx, t in enumerate(traces):
        for s in t["steps"]:
            rows.append({
                "trace_id": tidx,
                "step_id": s["step_id"],
                "node": s["node"],
                "tool": s["tool"],
            })
    return pd.DataFrame(rows)

def compute_behavior_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    total_steps = len(df)
    tool_calls = df["tool"].notna().sum()
    tool_usage_rate = tool_calls / total_steps if total_steps else 0

    tool_counts = df["tool"].value_counts(dropna=True).to_dict()
    node_counts = df["node"].value_counts().to_dict()

    return {
        "total_steps": total_steps,
        "tool_calls": tool_calls,
        "tool_usage_rate": tool_usage_rate,
        "tool_counts": tool_counts,
        "node_counts": node_counts,
    }
