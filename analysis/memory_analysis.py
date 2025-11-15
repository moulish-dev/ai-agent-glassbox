# analysis/memory_analysis.py

from typing import Dict, Any, List


def diff_memory(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute a simple diff between two memory snapshots.
    Returns dict with keys: added, removed, changed, unchanged.
    """
    before_keys = set(before.keys())
    after_keys = set(after.keys())

    added_keys = after_keys - before_keys
    removed_keys = before_keys - after_keys
    common_keys = before_keys & after_keys

    changed = {}
    unchanged = {}
    for k in common_keys:
        if before[k] != after[k]:
            changed[k] = {"before": before[k], "after": after[k]}
        else:
            unchanged[k] = before[k]

    return {
        "added": {k: after[k] for k in added_keys},
        "removed": {k: before[k] for k in removed_keys},
        "changed": changed,
        "unchanged": unchanged,
    }


def compute_memory_changes_for_trace(trace: dict) -> List[Dict[str, Any]]:
    """
    For a full trace (one AgentState as dict), compute memory diffs per step.
    Returns a list with one entry per step:
    {
      "step_id": ...,
      "node": ...,
      "diff": {added, removed, changed, unchanged}
    }
    """
    results = []
    for step in trace.get("steps", []):
        before = step.get("memory_before", {}) or {}
        after = step.get("memory_after", {}) or {}
        diff = diff_memory(before, after)
        results.append(
            {
                "step_id": step.get("step_id"),
                "node": step.get("node"),
                "diff": diff,
            }
        )
    return results
