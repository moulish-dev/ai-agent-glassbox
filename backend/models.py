from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class StepLog(BaseModel):
    step_id: int
    node: str
    thought: str
    tool: Optional[str] = None
    tool_input: Optional[Any] = None
    tool_output: Optional[Any] = None
    memory_before: Dict[str, Any]
    memory_after: Dict[str, Any]

class AgentState(BaseModel):
    user_query: str
    memory: Dict[str, Any] = {}
    steps: List[StepLog] = []
    final_answer: Optional[str] = None
