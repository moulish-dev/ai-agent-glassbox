# backend/graph.py

from typing import Dict, Any
from .models import AgentState, StepLog
from .agent import web_search_tool, summarize_tool
from .llm import gemini_llm 
from langsmith import Client
from langsmith import traceable
# load_env.py
from dotenv import load_dotenv
load_dotenv()
# load langsmith
client = Client()

# node 1: plan
@traceable(name="plan_node")
def plan_node(state: AgentState) -> AgentState:
    memory_before = state.memory.copy()
    prompt = (
        "You are an **investment research assistant**. "
        "The user will ask about stocks, ETFs, sectors, or macro topics.\n\n"
        f"User query: {state.user_query}\n\n"
        "Decide if you need web search to answer this.\n"
        "Think step by step about:\n"
        "- What assets or tickers are involved\n"
        "- Time horizon (short term / long term)\n"
        "- Key risk factors or metrics to look up\n"
        "Then say clearly whether you will SEARCH or NOT SEARCH."
    )
    plan = gemini_llm(prompt) 

    state.memory["plan"] = plan

    step = StepLog(
        step_id=len(state.steps) + 1,
        node="plan",
        thought=plan,
        tool="planning tool",
        tool_input=None,
        tool_output=None,
        memory_before=memory_before,
        memory_after=state.memory.copy(),
    )
    state.steps.append(step)
    
    # RETURN something serializable:
    return {
        "node": "plan",
        "thought": plan,
        "tool": "planning tool",
        "memory_after": state.memory,
    }, state

@traceable(name="research_node")
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

@traceable(name="answer_node")
def answer_node(state: AgentState) -> AgentState:
    memory_before = state.memory.copy()

    context = state.memory.get("research_raw", "No external research was used.")
    prompt = (
        "You are an **investment research assistant**.\n\n"
        f"User query: {state.user_query}\n"
        f"External research:\n{context}\n\n"
        "Write a structured, educational answer with sections like:\n"
        "- Business / asset overview\n"
        "- Recent news or catalysts\n"
        "- Key metrics or fundamentals (if mentioned)\n"
        "- Risks and uncertainties\n"
        "- Summary\n\n"
        "IMPORTANT: This is **not** financial advice. "
        "Be explicit that your answer is informational only."
    )
    answer = gemini_llm(prompt)
    state.final_answer = answer

    step = StepLog(
        step_id=len(state.steps) + 1,
        node="answer",
        thought="Generating final answer from context.",
        tool="answer_tool",
        tool_input=None,
        tool_output=None,
        memory_before=memory_before,
        memory_after=state.memory.copy(),
    )
    state.steps.append(step)
    return state

def run_agent(user_query: str) -> AgentState:
    
    state = AgentState(user_query=user_query)
    result, state = plan_node(state)
    state = research_node(state)
    state = answer_node(state)
    return state



