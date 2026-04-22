from datetime import datetime
from src.masks import mask_account_number, mask_card_number
import logging

# Константы для шаблонов вывода
ACCOUNT_MASK_TEMPLATE = "Счёт {}"
CARD_MASK_TEMPLATE = "{} {}"

def mask_account_card(input_string: str) -> str:
    """
    Обрабатывает строку с типом и номером карты/счёта и возвращает замаскированный номер.

    Args:
        input_string (str): строка с типом и номером

    Returns:
        str: строка с замаскированным номером
    """
    parts = input_string.strip().split()
    
    # Проверка на пустой список частей
    if not parts:
        return "Ошибка: пустая строка"
    
    number = parts[-1]  # последняя часть — номер
    
    is_account = any(word.lower() in input_string.lower() for word in ['счёт', 'account'])

    try:
        if is_account:
            masked_number = mask_account_number(number)
            return ACCOUNT_MASK_TEMPLATE.format(masked_number)
        else:
            # Считаем, что всё остальное — карта
            masked_number = mask_card_number(number)
            card_name = ' '.join(parts[:-1])
            return CARD_MASK_TEMPLATE.format(card_name, masked_number)
    except ValueError as e:
        return f"Ошибка: {e}"

def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: строка с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024")

    Raises:
        ValueError: если строка не соответствует ожидаемому формату
    """
    try:
        dt = datetime.fromisoformat(date_string)
        formatted_date = dt.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        logging.warning(f"Не удалось обработать дату: {date_string}")
        raise ValueError(
            f"Некорректный формат даты: {date_string}. "
            "Ожидаемый формат: YYYY-MM-DDTHH:MM:SS.ssssss"
        ) from e

def filter_by_state(transactions: list, state: str = 'EXECUTED') -> list:
    """Фильтрует список транзакций по значению поля 'state'."""
    return [
        transaction for transaction in transactions
        if transaction.get('state') == state and transaction.get('state') is not None
    ]

def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Сортирует список транзакций по дате."""
    def parse_date(date_str: str) -> datetime:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    
    return sorted(
        transactions,
        key=lambda x: parse_date(x.get('date', '9999-01-01')),  # дефолтная дата
        reverse=reverse
    )

class Widget:
    def __init__(self, transactions: list):
        """Инициализирует виджет с списком транзакций."""
        if not isinstance(transactions, list):
            raise TypeError("transactions должен быть списком")
        self.transactions = transactions

    def show_executed(self) -> list:
        """Возвращает отсортированный список выполненных транзакций."""
        filtered_transactions = filter_by_state(self.transactions)
        sorted_transactions = sort_by_date(filtered_transactions)
        return sorted_transactions