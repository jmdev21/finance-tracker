import os
import requests
from dotenv import load_dotenv

load_dotenv()

FINTUAL_BASE_URL = "https://fintual.cl/api"

def get_fintual_token() -> str:
    email = os.getenv("FINTUAL_EMAIL")
    password = os.getenv("FINTUAL_PASSWORD")

    if not email or not password:
        raise Exception("Credenciales de Fintual no encontradas")

    payload = {
        "user": {
            "email": email,
            "password": password
        }
    }

    response = requests.post(
        f"{FINTUAL_BASE_URL}/access_tokens",
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    try:
        return data["data"]["attributes"]["token"]
    except KeyError:
        raise Exception(f"Formato inesperado en respuesta Fintual: {data}")

