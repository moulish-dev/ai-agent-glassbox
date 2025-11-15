# run_once.py

from analysis.traces_loader import save_trace
from backend.graph import run_agent

def main():
    query = "Explain why world models are important for AI safety in simple terms."
    state = run_agent(query)
    save_trace(state, "trace_001_world_models")

    print("Trace saved to data/traces/trace_001_world_models.json")

if __name__ == "__main__":
    main()
