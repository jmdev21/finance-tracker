import csv
import os
import sys
import logging
from datetime import datetime

from collectors.fintual.fintual_goals import get_fintual_total
from collectors.racional.racional_valuation import get_racional_total
from collectors.binance.binance_funding import get_funding_total_usdt
from utils.fx import usd_to_clp


CSV_PATH = "database/historical_data.csv"

# -------------------------------------------------
# Configuración logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -------------------------------------------------
# Validación snapshot existente
# -------------------------------------------------
def snapshot_exists_today():
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(CSV_PATH):
        return False

    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] == today:
                return True

    return False


# -------------------------------------------------
# Obtener datos con validación fuerte
# -------------------------------------------------
def fetch_all_sources():
    try:
        logging.info("Obteniendo datos de Fintual...")
        total_fintual = get_fintual_total()
        if total_fintual is None:
            raise ValueError("Fintual retornó None")

        logging.info("Obteniendo datos de Racional...")
        total_racional = get_racional_total()
        if total_racional is None:
            raise ValueError("Racional retornó None")

        logging.info("Obteniendo datos de Binance...")
        total_binance_usdt = get_funding_total_usdt()
        if total_binance_usdt is None:
            raise ValueError("Binance retornó None")

        total_binance_clp = usd_to_clp(total_binance_usdt)

        logging.info("Todas las fuentes respondieron correctamente.")

        return total_fintual, total_racional, total_binance_clp

    except Exception as e:
        logging.error("❌ Error obteniendo datos:")
        logging.exception(e)
        sys.exit(1)  # Termina el script con error


# -------------------------------------------------
# Guardar snapshot
# -------------------------------------------------
def save_snapshot():
    today = datetime.now().strftime("%Y-%m-%d")

    total_fintual, total_racional, total_binance_clp = fetch_all_sources()

    total_patrimonio = (
        total_fintual +
        total_racional +
        total_binance_clp
    )

    file_exists = os.path.isfile(CSV_PATH)

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["date", "fintual", "racional", "binance", "total"])

        writer.writerow([
            today,
            total_fintual,
            total_racional,
            total_binance_clp,
            total_patrimonio
        ])

    logging.info("✅ Snapshot guardado correctamente.")


# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    if snapshot_exists_today():
        logging.warning("⚠ Ya existe snapshot de hoy. No se insertó nada.")
    else:
        save_snapshot()