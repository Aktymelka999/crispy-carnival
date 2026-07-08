import os

import requests
from dotenv import load_dotenv

# Загружаем переменные из .env (только для запуска вне тестов)
load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("EXCHANGE_API_KEY")


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Получает текущий курс валюты через API.
    Возвращает float: сколько target_currency стоит 1 единица base_currency.
    """
    if not API_KEY:
        raise ValueError("API ключ не найден. Проверьте переменную EXCHANGE_API_KEY в .env")

    headers = {"apikey": API_KEY}
    params = {"base": base_currency, "symbols": target_currency}

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()  # Выбросит ошибку, если статус не 2xx

    data = response.json()
    rates = data.get("rates", {})

    if target_currency not in rates:
        raise ValueError(f"Курс для валюты {target_currency} не найден")

    return float(rates[target_currency])


def convert_transaction_to_rub(transaction: dict) -> float:
    """
    Принимает транзакцию (dict) и возвращает сумму в рублях (float).

    Логика:
    - Если валюта RUB -> возвращаем amount.
    - Если USD или EUR -> запрашиваем курс и конвертируем.
    - Для остальных валют выбрасываем ошибку (или можно вернуть 0, зависит от требований).
    """
    amount = float(transaction.get("amount", 0))
    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        rate = get_exchange_rate(currency, "RUB")
        return amount * rate

    raise ValueError(f"Конвертация для валюты {currency} не поддерживается")
