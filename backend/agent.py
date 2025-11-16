import requests
import os
from valyu import Valyu
from dotenv import load_dotenv, dotenv_values
from langsmith.run_helpers import traceable

load_dotenv()
VALYU_API_KEY = os.getenv("VALYU_API_KEY")
valyu = Valyu(api_key=VALYU_API_KEY)

@traceable(name="web_search_tool")
def web_search_tool(query: str) -> str:
    finance_query = f"{query} -- extensive company or investment research and also stock OR ETF OR earnings OR financial results or about it"
    # Valyu DeepSearch API
    response = valyu.search(
        finance_query
    )
    content=""
    # Access results
    for result in response.results:
        content = result.content
        # print(f"Title: {result.title}")
        # print(f"URL: {result.url}")
        # print(f"Content: {result.content}")

    return f"[FINANCE SEARCH RESULTS for: {query}] ---> {content}"

@traceable(name="summarizing_tool")
def summarize_tool(text: str) -> str:

    response = valyu.answer(
        text,
        system_instructions="Summarize this"
    )

    # Access the answer
    summary = response.contents

    # Placeholder – later call LLM for summary
    return f"Summary of {text}: {summary}"
