# backend/llm.py

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3:1b"  # change to whatever model you use, e.g. "qwen2.5", "deepseek-r1", etc.

def ollama_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Call a local Ollama model and return the full response text.
    Requires:
      - Ollama running locally (ollama serve)
      - The model to be pulled.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,   # easier for now – no streaming
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
    except Exception as e:
        # Fallback so the rest of the pipeline doesn’t crash
        return f"[OLLAMA ERROR] {e} | PROMPT: {prompt[:200]}"
    
    data = resp.json()
    # Ollama returns: {"model": "...", "created_at": "...", "response": "...", ...}
    return data.get("response", "")
