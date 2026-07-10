import os
import requests
from decimal import Decimal
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

from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional

from .external_api import get_exchange_rate


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> Optional[Decimal]:
    """
    Конвертирует сумму транзакции в рубли.
    
    Ожидаемая структура:
    {
      "operationAmount": {
        "amount": 100.50,
        "currency": "USD"
      },
      ...
    }
    
    Возвращает Decimal (рубли) или None, если конвертация невозможна.
    """
    op_amount = transaction.get("operationAmount")
    
    
    if not isinstance(op_amount, dict):
        return None

    amount_raw = op_amount.get("amount")
    currency = op_amount.get("currency")

    if amount_raw is None or currency is None:
        return None

    
    try:
        amount = Decimal(str(amount_raw))
    except (InvalidOperation, ValueError, TypeError):
        return None

    currency_upper = currency.upper()

    
    if currency_upper == "RUB":
        return amount

    try:
        rate = get_exchange_rate(currency_upper, "RUB")
        return amount * rate
    except ValueError:
        return None