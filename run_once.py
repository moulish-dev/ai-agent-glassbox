# run_once.py
from uuid import uuid4
from analysis.traces_loader import save_trace
from backend.graph import run_agent
from langsmith.run_helpers import traceable


@traceable(name="glassmind-navigator")
def main(query):
    
    
    state = run_agent(query)
    trace_file_name = f"trace_{uuid4().hex}_{query[:10].replace(' ', '_')}.json"
    save_trace(state, trace_file_name)

    
    print(f"Trace saved to data/traces/{trace_file_name}")


if __name__ == "__main__":
    main("what command to use for sopying file in linux?")
