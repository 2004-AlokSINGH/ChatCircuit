import os
from dotenv import load_dotenv
from langchain_core.tools import tool, BaseTool

load_dotenv()
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch the latest stock price for a given stock symbol
    using the Alpha Vantage API.
    """
    import requests
    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}"
        f"&apikey={os.getenv('STOCK_API_KEY')}"
    )
    return requests.get(url).json()
