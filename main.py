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

def run_agent_with_query(query: str) -> str:
    """
    Run the agent on a given user query, save a trace,
    and return the trace name (without .json extension).
    """
    state = run_agent(query)

    # Make a clean trace name
    ts = uuid4().hex
    safe_snippet = "".join(c for c in query[:20] if c.isalnum() or c in ("-", "_")).rstrip()
    trace_name = f"trace_{ts}_{safe_snippet or 'query'}"

    save_trace(state, trace_name)
    return trace_name

if __name__ == "__main__":
    main("What does Valyu.ai do?")
