from collectors.binance.binance_auth import get_binance_client
from utils.numbers import truncate


def get_funding_balances():
    """
    Obtiene balances del Funding Wallet (Fondos).
    Retorna solo assets con amount > 0.
    """
    client = get_binance_client()
    funds = client.funding_wallet()

    #print(f"📦 FUNDING WALLET recibido: {len(funds)} assets")

    balances = []

    for f in funds:
        amount = float(f.get("free", 0))

        if amount > 0:
            balances.append({
                "asset": f["asset"],
                "amount": amount
            })

    #print(f"✅ Assets con balance > 0: {balances}")
    return balances


def get_funding_total_usdt() -> float:
    """
    Convierte el Funding Wallet completo a USDT.
    Ignora activos sin par USDT.
    """
    client = get_binance_client()
    balances = get_funding_balances()

    prices = {
        p["symbol"]: float(p["price"])
        for p in client.get_all_tickers()
    }

    #print(f"\n📈 Tickers disponibles: {len(prices)}")

    total = 0.0

    for b in balances:
        asset = b["asset"]
        amount = b["amount"]

        if asset == "USDT":
            total += amount
            print(f"USDT: {amount}")
            continue

        symbol = f"{asset}USDT"
        price = prices.get(symbol)

        if price:
            value = amount * price
            total += value
            #(f"{asset}: {amount} x {price} = {value:.4f} USDT")
        else:
            print(f"⚠️ {asset} sin par USDT → ignorado")

    return truncate(total)
