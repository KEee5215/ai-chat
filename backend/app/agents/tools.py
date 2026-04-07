"""自定义工具定义 - 使用 LangChain"""

from langchain.tools import tool
from typing import Optional
import requests


@tool
def calculator(expression: str) -> str:
    """
    A simple calculator tool for evaluating mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4")

    Returns:
        The result of the calculation as a string
    """
    try:
        # Only allow safe characters in the expression
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"

        # Safe evaluation using restricted scope
        allowed_names = {"__builtins__": {k: __builtins__[k] for k in ["abs", "sum", "min", "max", "pow", "round"]}}
        result = eval(expression, {"__builtins__": allowed_names}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"


@tool
def search(query: str, num_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo search API.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)

    Returns:
        Formatted search results
    """
    try:
        url = "https://api.duckduckgo.com/i/json"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        results = []
        if "RelatedTopics" in data:
            for i, topic in enumerate(data["RelatedTopics"][:num_results]):
                if "Text" in topic and "FirstURL" in topic:
                    results.append(f"{i+1}. {topic['Text']}\n   URL: {topic['FirstURL']}")

        if not results:
            return "No search results found."

        return "\n\n".join(results)
    except requests.RequestException as e:
        return f"Search failed: {str(e)}"
    except Exception as e:
        return f"Error performing search: {str(e)}"


# 可用的工具列表
TOOLS = [calculator, search]
