from typing import Generator, List, Dict, Any

Transaction = Dict[str, Any]

def filter_by_currency(
    transactions: list[Transaction],
    currency: str
) -> Generator[Transaction, None, None]:
    """
    Фильтрует транзакции по валюте (регистронезависимо).
    """
    if not isinstance(transactions, list):
        raise TypeError("Транзакции должны быть списком")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue
        if ('operationAmount' in transaction and
            isinstance(transaction['operationAmount'], dict) and
            'currency' in transaction['operationAmount'] and
            transaction['operationAmount']['currency'].lower() == currency.lower()):
            yield transaction

from typing import Iterator, List, Dict

def transaction_descriptions(transactions: List[Dict]) -> Iterator[str]:
    """
    Генератор, возвращающий описание каждой транзакции по очереди.

    Args:
        transactions (List[Dict]): Список словарей с данными о транзакциях.
                                 Каждый словарь должен содержать ключ 'description'.

    Yields:
        str: Описание текущей транзакции.
    """
    for transaction in transactions:
        if 'description' in transaction:
            yield transaction['description']
        else:
            yield "Описание отсутствует"

def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генератор номеров карт в заданном диапазоне.

    Генерирует строки с номерами карт (например, '1234567890123456')
    в диапазоне от `start` до `stop` (включительно).
    Номера форматируются как 16-значные строки с ведущими нулями.

    Args:
        start (int): Начальное число диапазона (например, 123456789012345).
        stop (int): Конечное число диапазона (например, 123456789012350).

    Yields:
        str: 16-значный номер карты (с ведущими нулями, если нужно).
    """
    for num in range(start, stop + 1):
        yield f"{num:016d}" 

def description_generator(transactions):
    for transaction in transactions:
        if 'description' in transaction:
            yield transaction['description']
        else:
            yield "Описание отсутствует"

def transaction_descriptions(transactions):
    """
    Генератор, который извлекает описания транзакций из списка транзакций.

    Args:
        transactions (list): Список словарей, представляющих транзакции.
            Каждая транзакция может содержать поле 'description'.

    Yields:
        str: Описание транзакции, если поле 'description' присутствует.
            Иначе — строка "Описание отсутствует".

    Raises:
        TypeError: Если входной параметр не является итерируемым или равен None.
        KeyError: Если элемент в списке транзакций не является словарем
            и не содержит ожидаемых полей.
    """
    if transactions is None:
        raise TypeError("Input cannot be None")

    try:
        for transaction in transactions:
            if not isinstance(transaction, dict):
                raise KeyError("Each transaction must be a dictionary")
            if 'description' in transaction:
                yield transaction['description']
            else:
                yield "Описание отсутствует"
    except TypeError:
        raise TypeError("Input must be an iterable")
    
def card_number_generator(start, end):
    """
    Генератор номеров карт с дополнением до 16 знаков ведущими нулями.

    Args:
        start (int): Начальный номер карты.
        end (int): Конечный номер карты (включительно).

    Yields:
        str: Номер карты в виде 16‑значной строки с ведущими нулями.
    Raises:
        ValueError: Если start или end отрицательные.
        TypeError: Если start/end не являются целыми числами.
    """
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Start and end must be integers")
    if start < 0 or end < 0:
        raise ValueError("Card numbers cannot be negative")

    for number in range(start, end + 1):
        yield f"{number:016d}"