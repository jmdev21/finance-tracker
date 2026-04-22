import os
import sys
import logging
from datetime import datetime

from supabase import create_client

from collectors.fintual.fintual_goals import get_fintual_goals
from collectors.racional.racional_valuation import get_racional_total
from collectors.binance.binance_funding import get_bitcoin_total_clp

# -------------------------------------------------
# Configuración logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# Configuración Supabase
# -------------------------------------------------
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    logging.error("❌ Faltan variables de entorno de Supabase.")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# -------------------------------------------------
# Validación snapshot existente (en Supabase)
# -------------------------------------------------
def snapshot_exists_today():
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        response = supabase.table("historical_data") \
            .select("date") \
            .eq("date", today) \
            .execute()

        return len(response.data) > 0

    except Exception as e:
        logging.error("❌ Error verificando snapshot existente:")
        logging.exception(e)
        sys.exit(1)

# -------------------------------------------------
# Obtener datos con validación fuerte
# -------------------------------------------------
def fetch_all_sources():
    try:
        logging.info("Obteniendo datos de Fintual...")
        total_fintual = get_fintual_goals()
        if total_fintual is None:
            raise ValueError("Fintual retornó None")

        logging.info("Obteniendo datos de Racional...")
        total_racional = get_racional_total()
        if total_racional is None:
            raise ValueError("Racional retornó None")

        logging.info("Obteniendo valor de Bitcoin desde Yahoo...")
        total_binance_clp = get_bitcoin_total_clp()
        if total_binance_clp is None:
            raise ValueError("Binance retornó None")

        logging.info("Todas las fuentes respondieron correctamente.")

        return total_fintual, total_racional, total_binance_clp

    except Exception as e:
        logging.error("❌ Error obteniendo datos:")
        logging.exception(e)
        sys.exit(1)

# -------------------------------------------------
# Guardar snapshot en Supabase
# -------------------------------------------------
def save_snapshot():
    today = datetime.now().strftime("%Y-%m-%d")

    total_fintual, total_racional, total_binance_clp = fetch_all_sources()

    total_patrimonio = (
        total_fintual +
        total_racional +
        total_binance_clp
    )

    data = {
        "date": today,
        "fintual": total_fintual,
        "racional": total_racional,
        "binance": total_binance_clp,
        "total": total_patrimonio
    }

    try:
        supabase.table("historical_data").insert(data).execute()
        logging.info("✅ Snapshot guardado correctamente en Supabase.")

    except Exception as e:
        logging.error("❌ Error insertando snapshot:")
        logging.exception(e)
        sys.exit(1)

# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":
    if snapshot_exists_today():
        logging.warning("⚠ Ya existe snapshot de hoy. No se insertó nada.")
    else:
        save_snapshot()
