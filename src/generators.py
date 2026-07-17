import random
from typing import Any, Dict, List, Optional


def filter_by_currency(transactions: Optional[List[Any]], currency: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте, безопасно обрабатывая «мусорные» данные.

    - Пропускает элементы, которые не являются dict.
    - Пропускает элементы без ключа 'currency'.
    - Если на вход пришёл не список — возвращает пустой список.
    """
    if not isinstance(transactions, list):
        return []

    result: List[Dict[str, Any]] = []
    for t in transactions:
        if not isinstance(t, dict):
            continue
        if "currency" not in t:
            continue
        if t["currency"] == currency:
            result.append(t)
    return result


def card_number_generator(length: int, count: int) -> List[str]:
    if length <= 0 or count <= 0:
        return []
    numbers: List[str] = []
    for _ in range(count):
        number = "".join(str(random.randint(0, 9)) for _ in range(length))
        numbers.append(number)
    return numbers


def description_generator(count: int) -> List[str]:
    templates = [
        "Оплата покупки в интернет-магазине",
        "Перевод другу на карту",
        "Снятие наличных в банкомате",
        "Пополнение баланса телефона",
        "Оплата подписки на сервис",
        "Покупка билетов на поезд",
        "Оплата заказа в кафе",
        "Возврат средств за товар",
        "Платеж по кредиту",
        "Оплата ЖКХ услуг",
    ]
    if count <= 0:
        return []
    descriptions: List[str] = []
    for i in range(count):
        descriptions.append(f"{templates[i % len(templates)]} #{i + 1}")
    return descriptions


def transaction_descriptions(count: int) -> List[str]:

    return description_generator(count)
