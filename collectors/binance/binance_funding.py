import os
import yfinance as yf
from utils.numbers import truncate
from utils.fx import usd_to_clp

def get_bitcoin_total_clp() -> float:
    """
    Calcula el valor total de tu BTC en CLP usando Yahoo Finance y la cantidad guardada en secrets.
    """
    # Tomamos la cantidad desde el secreto
    btc_amount = float(os.getenv("BINANCE_BTC_AMOUNT", 0))
    if btc_amount <= 0:
        raise Exception("BINANCE_BTC_AMOUNT no definido o es 0")

    # Obtenemos precio actual de BTC en USD
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="1d")
    if data.empty:
        raise Exception("No se pudo obtener el precio de Bitcoin desde Yahoo Finance")
    
    btc_price_usd = float(data['Close'].iloc[-1])

    # Calculamos total en USD
    total_usd = btc_amount * btc_price_usd

    # Convertimos a CLP
    total_clp = usd_to_clp(total_usd)

    return truncate(total_clp)

