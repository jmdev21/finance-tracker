import os
import requests
from dotenv import load_dotenv

from collectors.fintual.fintual_auth import get_fintual_token

load_dotenv()

FINTUAL_BASE_URL = "https://fintual.cl/api"

def get_fintual_goals():
    token = get_fintual_token()
    email = os.getenv("FINTUAL_EMAIL")

    if not email:
        raise Exception("FINTUAL_EMAIL no está definido en el .env")

    params = {
        "user_email": email,
        "user_token": token
    }

    response = requests.get(
        f"{FINTUAL_BASE_URL}/goals",
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["data"]

def get_fintual_total() -> int:
    goals = get_fintual_goals()

    total = 0

    for goal in goals:
        attrs = goal.get("attributes", {})
        nav = attrs.get("nav")

        if nav is None:
            continue

        total += int(nav)

    return total


