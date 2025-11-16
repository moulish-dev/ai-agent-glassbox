import requests
import os
from valyu import Valyu
from dotenv import load_dotenv, dotenv_values

load_dotenv()
VALYU_API_KEY = os.get_env("VALYU_API_KEY")
valyu = Valyu(api_key=VALYU_API_KEY)

def web_search_tool(query: str) -> str:

    # Valyu DeepSearch API
    response = valyu.search(
        query
    )
    content=""
    # Access results
    for result in response.results:
        content = result.content
        # print(f"Title: {result.title}")
        # print(f"URL: {result.url}")
        # print(f"Content: {result.content}")

    # Replace with real search API if you want
    return f"[SEARCH RESULTS for: {query}] ---> {content}"

def summarize_tool(text: str) -> str:

    response = valyu.answer(
        text,
        system_instructions="Summarize this"
    )

    # Access the answer
    summary = response.contents

    # Placeholder – later call LLM for summary
    return f"Summary of {text}: {summary}"
