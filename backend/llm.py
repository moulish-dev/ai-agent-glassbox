# backend/llm.py
import os
from langsmith import traceable
import google.generativeai as genai

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

genai.configure(api_key=GEMINI_API_KEY)

# pick your model; gemini-1.5-flash is fast + cheap
DEFAULT_MODEL = "gemini-2.5-flash-lite"


@traceable(name="gemini_llm", run_type="llm")
def gemini_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Calls the Google Gemini model and returns a plain string.
    LangSmith will capture prompt + output + timing automatically.
    """
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(prompt)
    except Exception as e:
        raise RuntimeError(f"Gemini API error: {e}") from e

    # Extract text safely
    if not response or not hasattr(response, "text"):
        raise RuntimeError("Gemini returned empty response or invalid structure.")

    return response.text
