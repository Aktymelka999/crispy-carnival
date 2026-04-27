from datetime import datetime

from src.masks import mask_account_number, mask_card_number


def mask_account_card(input_string: str) -> str:
    """
    Обрабатывает строку с типом и номером карты/счёта и возвращает замаскированный номер.

    Args:
        input_string (str): строка с типом и номером

    Returns:
        str: строка с замаскированным номером
    """
    if not input_string or not input_string.strip():
        return "Ошибка: пустая строка"

    parts = input_string.strip().split()
    if len(parts) < 2:
        return "Ошибка: недостаточно данных в строке"

    number = parts[-1]  # последняя часть — номер

    is_account = any(word.lower() in input_string.lower() for word in ['счёт', 'счет', 'account'])

    try:
        if is_account:
            masked_number = mask_account_number(number)
            return f"Счёт {masked_number}"
        else:
            # Считаем, что всё остальное — карта
            masked_number = mask_card_number(number)
            card_name = ' '.join(parts[:-1])
            return f"{card_name} {masked_number}"
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
    if not date_string:
        raise ValueError("Пустая строка даты")

    # Убираем Z в конце, если есть
    date_string_clean = date_string.rstrip('Z')

    try:
        dt = datetime.fromisoformat(date_string_clean)
        formatted_date = dt.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        raise ValueError(
            f"Некорректный формат даты: {date_string}. "
            "Ожидаемый формат: YYYY-MM-DDTHH:MM:SS.ssssss"
        ) from e

def filter_by_state(transactions: list, state: str = 'EXECUTED') -> list:
    """Фильтрует список транзакций по значению поля 'state'."""
    if not transactions:
        return []
    return [transaction for transaction in transactions if transaction.get('state') == state]

def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """Сортирует список транзакций по дате."""
    if not transactions:
        return []

    def parse_date(date_str: str) -> datetime:
        # Убираем Z в конце, если есть
        clean_date_str = date_str.rstrip('Z')
        try:
            return datetime.fromisoformat(clean_date_str)
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {date_str}")

    return sorted(transactions, key=lambda x: parse_date(x['date']), reverse=reverse)

# Существующий код виджета...
class Widget:
    def __init__(self, transactions):
        self.transactions = transactions

    def show_executed(self):
        executed = filter_by_state(self.transactions)
        sorted_executed = sort_by_date(executed)
        return sorted_executed