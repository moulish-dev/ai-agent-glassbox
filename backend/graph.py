# backend/graph.py

from typing import Dict, Any
from .models import AgentState, StepLog
from .agent import web_search_tool, summarize_tool
from .llm import ollama_llm  # 👈 add this

# node 1: plan
def plan_node(state: AgentState) -> AgentState:
    memory_before = state.memory.copy()
    prompt = f"You are a research agent. User query: {state.user_query}. Decide if you need web search."
    plan = ollama_llm(prompt)  # 👈 use mock LLM

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

def research_node(state: AgentState) -> AgentState:
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

def answer_node(state: AgentState) -> AgentState:
    memory_before = state.memory.copy()

    context = state.memory.get("research_raw", "No external research was used.")
    prompt = f"User query: {state.user_query}\nContext: {context}\nCompose a helpful answer."
    answer = ollama_llm(prompt)  # 👈 use mock LLM
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

def run_agent(user_query: str) -> AgentState:
    state = AgentState(user_query=user_query)
    state = plan_node(state)
    state = research_node(state)
    state = answer_node(state)
    return state



