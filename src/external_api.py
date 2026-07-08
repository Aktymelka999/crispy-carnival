
import os
import requests
from decimal import Decimal
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY не найден. Проверьте .env")

BASE_URL = "https://api.exchangerate.host/latest" 

def get_exchange_rate(base_currency: str, target_currency: str) -> Optional[Decimal]:
    params = {
        "base": base_currency.upper(),
        "symbols": target_currency.upper()
    }

    headers = {
        "X-API-Key": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()

        rates = data.get("rates", {})
        rate_value = rates.get(target_currency.upper())

        if rate_value is None:
            return None

        return Decimal(str(rate_value))
    except (requests.RequestException, ValueError, KeyError):
        return None


def convert_transaction_amount(transaction: Dict[str, Any]) -> Optional[Decimal]:
    amount = transaction.get("amount")
    currency = transaction.get("currency")
    target_currency = transaction.get("target_currency")

    if amount is None or currency is None or target_currency is None:
        return None

    rate = get_exchange_rate(currency, target_currency)
    if rate is None:
        return None

    try:
        amount_dec = Decimal(str(amount))
    except Exception:
        return None

    return amount_dec * rate