from agents import function_tool
from tavily import TavilyClient
import simpleeval
from app.core.settings import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


@function_tool
def search_web(query: str, label: str | None = None):
    """
    Search the web from information using Tavily API

    query : The search query to use.
    label : The label to use to tell what you are currently doing with this tool.
    """
    results = tavily_client.search(query, max_results=5)
    return results


@function_tool
def calculate(expression: str, description: str) -> str:
    """
    Calculate mathematical expression safely.
    Use this tool to:
    - Calculate discounts (e.g., original_price * 0.9 for 10% discount)
    - Calculate totals (e.g., price1 + price2 + shipping)
    - Convert currencies (e.g., usd_price * 15000)
    - Compare costs (e.g., product_a - product_b)

    expression: Mathematical expression to calculate (e.g., "500000 * 0.9", "100 + 50 + 25")
    description: What you are calculating (e.g., "Calculate 10% discount from 500000")

    Returns:
    The result of the calculation with the description
    """
    try:
        result = simpleeval.simple_eval(expression)
        return f"{description}: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"
