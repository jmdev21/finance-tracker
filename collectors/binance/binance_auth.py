import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


def get_binance_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise Exception("BINANCE_API_KEY o BINANCE_API_SECRET no están definidos")

    client = Client(api_key, api_secret)
    return client
