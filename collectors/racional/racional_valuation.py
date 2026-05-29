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

    # NUEVO ETF ESGV
    esgv_shares = float(os.getenv("RACIONAL_ESGV_SHARES", 0))

    # Wallet USD
    usd_balance = float(os.getenv("RACIONAL_USD_BALANCE", 0))

    print("RAW USD:", repr(usd_balance))

    if usd_balance == 0:
        print("error al obtener valor del dolar en variable")

    # Precios actuales
    ltm_price = get_price_yahoo_web("LTM.SN")
    meta_price = get_price("META")
    amzn_price = get_price("AMZN")

    # NUEVO
    esgv_price = get_price("ESGV")

    # Valorizaciones
    ltm_value = ltm_shares * ltm_price

    meta_value = usd_to_clp(meta_shares * meta_price)
    amzn_value = usd_to_clp(amzn_shares * amzn_price)

    # NUEVO
    esgv_value = usd_to_clp(esgv_shares * esgv_price)

    # Wallet USD
    usd_wallet_value = usd_to_clp(usd_balance)

    if usd_wallet_value == 0:
        print("error al obtener valor del dolar en funcion a clp")

    print(f"Valor dolares: {usd_wallet_value}")
    print(f"Valor ESGV: {esgv_value}")

    total = (
        ltm_value
        + meta_value
        + amzn_value
        + esgv_value
        + usd_wallet_value
    )

    return {
        "total": total
    }


def get_racional_total() -> int:
    valuation = get_racional_valuation()
    return int(valuation["total"])
