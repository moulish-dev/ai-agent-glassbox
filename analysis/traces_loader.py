import json
from pathlib import Path
from typing import List
from backend.models import AgentState

TRACES_DIR = Path("data/traces")

def save_trace(state: AgentState, trace_name: str) -> Path:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    path = TRACES_DIR / f"{trace_name}.json"
    with path.open("w") as f:
        json.dump(state.model_dump(), f, indent=2)
    return path

def load_traces() -> List[dict]:
    traces = []
    for p in TRACES_DIR.glob("*.json"):
        with p.open() as f:
            traces.append(json.load(f))
    return traces
