def filter_by_currency(transactions, currency):
    """Фильтрует транзакции по валюте.

    Args:
        transactions: список транзакций.
        currency: валюта для фильтрации (строка).

    Yields:
        Транзакции, где operationAmount.currency совпадает с currency (с учётом регистра).
    """
    if not isinstance(transactions, list):
        raise TypeError("transactions must be a list")

    currency_lower = currency.lower() if currency is not None else None

    for transaction in transactions:
        if not isinstance(transaction, dict):
            continue

        operation_amount = transaction.get("operationAmount")
        if not isinstance(operation_amount, dict):
            continue

        curr = operation_amount.get("currency")
        if curr is None:
            continue

        if curr.lower() == currency_lower:
            yield transaction


def description_generator(transactions):
    """Генерирует описания транзакций.

    Args:
        transactions: список транзакций.

    Yields:
        Описание транзакции или «Описание отсутствует», если поля description нет.
    """
    if transactions is None:
        raise TypeError("transactions cannot be None")

    if not hasattr(transactions, '__iter__'):
        raise TypeError("transactions must be iterable")

    for transaction in transactions:
        if not isinstance(transaction, dict):
            raise KeyError("Each transaction must be a dict")

        description = transaction.get("description")
        yield description if description is not None else "Описание отсутствует"


def card_number_generator(start, end):
    """Генерирует номера карт в диапазоне от start до end включительно.

    Args:
        start: начальный номер карты (целое число >= 0).
        end: конечный номер карты (целое число >= start).

    Yields:
        Номера карт в виде 16‑значных строк с ведущими нулями.
    """
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if start < 0 or end < 0:
        raise ValueError("start and end must be non-negative")
    if start > end:
        return

    for number in range(start, end + 1):
        yield f"{number:016d}"

def transaction_descriptions(transactions):
    """
    Генератор, возвращающий описания транзакций по очереди.

    Args:
        transactions (list): список словарей с данными о транзакциях.
            Каждый словарь может содержать ключ 'description'.

    Yields:
        str: описание транзакции, если оно есть; иначе — «Описание отсутствует».
    """
    for transaction in transactions:
        if isinstance(transaction, dict) and 'description' in transaction:
            description = transaction['description']
            if description is not None and description != '':
                yield description
            else:
                yield "Описание отсутствует"
        else:
            yield "Описание отсутствует"
