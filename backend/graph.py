from typing import Dict, Any
from .models import AgentState, StepLog
from .agent import web_search_tool, summarize_tool

# node 1: plan
def plan_node(state: AgentState, llm) -> AgentState:
    memory_before = state.memory.copy()
    # Call LLM to decide plan
    prompt = f"You are a research agent. User query: {state.user_query}. Decide if you need web search."
    plan = llm(prompt)

    state.memory["plan"] = plan

    step = StepLog(
        step_id=len(state.steps) + 1,
        node="plan",
        thought=plan,
        tool=None,
        tool_input=None,
        tool_output=None,
        memory_before=memory_before,
        memory_after=state.memory.copy(),
    )
    state.steps.append(step)
    return state

# node 2: maybe call tool
def research_node(state: AgentState, llm) -> AgentState:
    memory_before = state.memory.copy()

    if "search" in state.memory.get("plan", "").lower():
        tool_input = state.user_query
        tool_output = web_search_tool(tool_input)
        state.memory["research_raw"] = tool_output

        step = StepLog(
            step_id=len(state.steps) + 1,
            node="research",
            thought="Using web_search_tool based on plan.",
            tool="web_search_tool",
            tool_input=tool_input,
            tool_output=tool_output,
            memory_before=memory_before,
            memory_after=state.memory.copy(),
        )
        state.steps.append(step)
    else:
        step = StepLog(
            step_id=len(state.steps) + 1,
            node="research",
            thought="Skipping web search, plan said no.",
            tool=None,
            tool_input=None,
            tool_output=None,
            memory_before=memory_before,
            memory_after=state.memory.copy(),
        )
        state.steps.append(step)
    return state

# node 3: final answer
def answer_node(state: AgentState, llm) -> AgentState:
    memory_before = state.memory.copy()

    context = state.memory.get("research_raw", "No external research was used.")
    prompt = f"User query: {state.user_query}\nContext: {context}\nCompose a helpful answer."
    answer = llm(prompt)
    state.final_answer = answer

    step = StepLog(
        step_id=len(state.steps) + 1,
        node="answer",
        thought="Generating final answer from context.",
        tool=None,
        tool_input=None,
        tool_output=None,
        memory_before=memory_before,
        memory_after=state.memory.copy(),
    )
    state.steps.append(step)
    return state

# wrapper
def run_agent(user_query: str, llm) -> AgentState:
    state = AgentState(user_query=user_query)
    state = plan_node(state, llm)
    state = research_node(state, llm)
    state = answer_node(state, llm)
    return state


from analysis.traces_loader import save_trace

state = run_agent("Explain quantum computing to a beginner", llm)
save_trace(state, "trace_001_quantum_intro")

def plan_node(state: AgentState, llm, config) -> AgentState:
    # Maybe later you use past behavior metrics to adjust config.enable_search_threshold
    ...
