import os
from dotenv import load_dotenv
import yfinance as yf
from utils.fx import usd_to_clp


load_dotenv()


def get_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")

    if hist.empty:
        raise ValueError(f"No se pudo obtener precio para {ticker}")

    return float(hist["Close"].iloc[-1])

import yfinance as yf

def get_price_yahoo_web(ticker: str) -> float:
    stock = yf.Ticker(ticker)
    price = stock.info.get("regularMarketPrice")

    if price is None:
        raise ValueError(f"No se pudo obtener regularMarketPrice para {ticker}")

    return float(price)




def get_racional_valuation():
    # Cantidades desde .env
    ltm_shares = float(os.getenv("RACIONAL_LTM_SHARES", 0))
    meta_shares = float(os.getenv("RACIONAL_META_SHARES", 0))
    amzn_shares = float(os.getenv("RACIONAL_AMZN_SHARES", 0))
    msft_shares = float(os.getenv("RACIONAL_MSFT_SHARES", 0))

    # Precios actuales
    ltm_price = get_price_yahoo_web("LTM.SN")
    meta_price = get_price("META")
    amzn_price = get_price("AMZN")
    msft_price = get_price("MSFT")

    # Valorizaciones
    ltm_value = ltm_shares * ltm_price

    meta_value = meta_shares * meta_price
    meta_value = usd_to_clp(meta_value)

    amzn_value = amzn_shares * amzn_price
    amzn_value = usd_to_clp(amzn_value)

    msft_value = msft_shares * msft_price
    msft_value = usd_to_clp(msft_value)

    #print(f"{ltm_value} ,  {meta_value}  , {amzn_value} ,  {msft_value}")

    total = ltm_value + meta_value + amzn_value + msft_value

    return {
        "total": total
    }

def get_racional_total() -> int:
    valuation = get_racional_valuation()
    return int(valuation["total"])

