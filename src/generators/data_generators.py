from typing import Generator, Dict, Any, Optional

Transaction = Dict[str, Any]
CurrencyData = Dict[str, str]

OperationAmount = Dict[str, str | CurrencyData]

def filter_by_currency(
    transactions: list[Transaction],
    currency: str
) -> Generator[Transaction, None, None]:
    """
    Фильтрует транзакции по валюте.
    """
    for transaction in transactions:
        if 'operationAmount' in transaction:
            amount_data: OperationAmount = transaction['operationAmount']
            if 'currency' in amount_data:
                currency_data = amount_data['currency']
                if isinstance(currency_data, dict):
                    currency_dict: CurrencyData = currency_data
                    if currency_dict.get('name') == currency:
                        yield transaction
                elif isinstance(currency_data, str) and currency_data == currency:
                    yield transaction

def transaction_descriptions(
    transactions: list[Transaction]
) -> Generator[str, None, None]:
    """
    Извлекает описания транзакций.
    """
    for transaction in transactions:
        if 'description' in transaction:
            yield transaction['description']

def card_number_generator(
    start: int,
    end: int
) -> Generator[str, None, None]:
    """
    Генератор номеров карт.
    """
    # Валидация входных данных
    if start <= 0:
        raise ValueError("Начальное значение должно быть в диапазоне 1–9999999999999999")
    if end > 9999999999999999:
        raise ValueError("Конечное значение должно быть в диапазоне 1–9999999999999999")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    for num in range(start, end + 1):
        # Форматируем номер карты: XXXX XXXX XXXX XXXX
        card_str = f"{num:016d}"  # Дополняем нулями до 16 цифр
        formatted = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
        yield formatted