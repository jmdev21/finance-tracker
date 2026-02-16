import yfinance as yf


def get_price(ticker: str) -> float:
    stock = yf.Ticker(ticker)

    # precio más confiable para "ahora"
    price = stock.fast_info.get("last_price")

    if price is None:
        raise RuntimeError(f"No se pudo obtener precio para {ticker}")

    return float(price)
