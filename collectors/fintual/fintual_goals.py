import requests
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

FONDOS = [
    {
        "nombre": "Risky Norris",
        "id":     186,
        "cuotas": float(os.getenv("CUOTAS_RISKY_NORRIS", 0)),
    },
    {
        "nombre": "Very Conservative Streep",
        "id":     15077,
        "cuotas": float(os.getenv("CUOTAS_CONSERVATIVE_STREEP", 0)),
    },
]


def _obtener_valor_cuota(asset_id: int) -> float:
    hoy   = date.today()
    desde = hoy - timedelta(days=7)

    r = requests.get(
        f"https://fintual.cl/api/real_assets/{asset_id}/days",
        params={"from_date": desde.isoformat(), "to_date": hoy.isoformat()},
        timeout=15
    )

    if r.status_code != 200:
        raise Exception(f"Error en API ({asset_id}): {r.status_code} - {r.text[:200]}")

    datos = r.json().get("data", [])
    if not datos:
        raise Exception(f"Sin datos recientes para fondo {asset_id}.")

    return float(datos[-1]["attributes"].get("price", 0))


def get_fintual_goals() -> int:
    cuotas_risky       = float(os.getenv("CUOTAS_RISKY_NORRIS", 0))
    cuotas_conservative = float(os.getenv("CUOTAS_CONSERVATIVE_STREEP", 0))
 
    valor_risky       = _obtener_valor_cuota(186)
    valor_conservative = _obtener_valor_cuota(15077)
 
    total_risky       = cuotas_risky * valor_risky
    total_conservative = cuotas_conservative * valor_conservative
 
    return int(total_risky + total_conservative)

