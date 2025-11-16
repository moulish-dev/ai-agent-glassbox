# analysis/memory_analysis.py

from typing import Dict, Any, List

def dict_diff(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Return only the keys that changed between before and after."""
    diff = {}

    # keys changed or added
    for key in after:
        if key not in before or before[key] != after[key]:
            diff[key] = {"before": before.get(key), "after": after[key]}

    # keys removed
    for key in before:
        if key not in after:
            diff[key] = {"before": before[key], "after": None}

    return diff


def compute_memory_timeline(trace: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    For each step, compute memory diff.
    Returns list of: { step_id, node, diff }
    """
    timeline = []

    for step in trace["steps"]:
        before = step["memory_before"]
        after = step["memory_after"]

        diff = dict_diff(before, after)

        timeline.append({
            "step_id": step["step_id"],
            "node": step["node"],
            "diff": diff,
        })

    return timeline
