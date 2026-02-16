import yfinance as yf
from utils.numbers import truncate


def get_usd_clp_rate() -> float:
    """
    Obtiene el tipo de cambio USD → CLP usando Yahoo Finance.
    """
    usdclp = yf.Ticker("USDCLP=X")
    hist = usdclp.history(period="1d")

    if hist.empty:
        raise ValueError("No se pudo obtener el tipo de cambio USD/CLP")

    return float(hist["Close"].iloc[-1])


def usd_to_clp(amount_usd: float) -> int:
    """
    Convierte un monto en USD a CLP.
    """
    rate = get_usd_clp_rate()
    total = amount_usd * rate
    
    return int(truncate(total,0))
