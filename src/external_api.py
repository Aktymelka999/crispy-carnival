import os
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("EXCHANGE_API_KEY")


def get_exchange_rate(base_currency: str, target_currency: str) -> Decimal:
    """
    Получает текущий курс валюты через API.
    Возвращает Decimal: сколько target_currency стоит 1 единица base_currency.
    """
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте переменную EXCHANGE_API_KEY в .env")

    headers = {"apikey": API_KEY}
    params = {"base": base_currency, "symbols": target_currency}

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    rates = data.get("rates", {})

    if target_currency not in rates:
        raise ValueError(f"Курс для валюты {target_currency} не найден")

    return Decimal(str(rates[target_currency]))


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> Optional[Decimal]:
    """
    Конвертирует сумму транзакции в рубли.

    Поддерживает два формата поля currency:
      1. {"code": "USD"}  (новый формат)
      2. "USD"           (старый формат, fallback)

    Возвращает Decimal (рубли) или None, если конвертация невозможна.
    """
    op_amount = transaction.get("operationAmount")
    if not isinstance(op_amount, dict):
        return None

    amount_raw = op_amount.get("amount")
    currency_raw = op_amount.get("currency")

    if amount_raw is None or currency_raw is None:
        return None

    # Безопасное получение кода валюты
    if isinstance(currency_raw, dict):
        currency = currency_raw.get("code")
    else:
        currency = str(currency_raw).strip()

    if not currency or not isinstance(currency, str):
        return None

    try:
        amount = Decimal(str(amount_raw))
    except InvalidOperation, ValueError, TypeError:
        return None

    currency_upper = currency.upper()

    if currency_upper == "RUB":
        return amount

    try:
        rate = get_exchange_rate(currency_upper, "RUB")
        return amount * rate
    except ValueError:

        return None
