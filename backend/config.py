from pydantic import BaseModel

class AgentConfig(BaseModel):
    enable_search_threshold: float = 0.4  # probability or heuristic
    max_steps: int = 10

DEFAULT_CONFIG = AgentConfig()
