import os
from dotenv import load_dotenv

load_dotenv()

RACIONAL_HOLDINGS = [
    {
        "name": "LATAM Airlines",
        "ticker": "LTM.SN",
        "shares": float(os.getenv("RACIONAL_LTM_SHARES", 0)),
        "currency": "CLP",
    },
    {
        "name": "ETF S&P500 Chile",
        "ticker": "CFISP500.SN",
        "shares": float(os.getenv("RACIONAL_CFISP500_SHARES", 0)),
        "currency": "CLP",
    },
    {
        "name": "Meta Platforms",
        "ticker": "META",
        "shares": float(os.getenv("RACIONAL_META_SHARES", 0)),
        "currency": "USD",
    },
    
    {
        "name": "Amazon",
        "ticker": "AMZN",
        "shares": float(os.getenv("RACIONAL_AMZN_SHARES", 0)),
        "currency": "USD",
    },
    {
        "name": "Microsoft",
        "ticker": "MSFT",
        "shares": float(os.getenv("RACIONAL_MSFT_SHARES", 0)),
        "currency": "USD",
    }
]
