def filter_by_state(data, state):
    raise NotImplementedError("Function not implemented yet")


def sort_by_date(data, reverse=True):
    raise NotImplementedError("Function not implemented yet")


def filter_by_state(data, state):
    """
    Фильтрует список словарей по значению поля 'state'.


    Args:
        data (list): список словарей с данными
        state (str): значение поля state для фильтрации


    Returns:
        list: отфильтрованный список словарей
    """
    if not data:
        return []
    return [item for item in data if item.get("state") == state]



def sort_by_date(data, reverse=True):
    """
    Сортирует список словарей по полю 'date' в формате YYYY-MM-DD.

    Args:
        data (list): список словарей с полем 'date'
        reverse (bool): порядок сортировки (True — убывание, False — возрастание)

    Returns:
        list: отсортированный список словарей
    Raises:
        ValueError: при некорректном формате даты или отсутствии поля 'date'
    """
    if not data:
        return []

    def parse_date(item):
        try:
            return datetime.strptime(item["date"], "%Y-%m-%d")
        except KeyError:
            raise ValueError("Missing date field")
        except ValueError:
            raise ValueError(f"Invalid date format: {item['date']}")

    return sorted(data, key=parse_date, reverse=reverse)

from datetime import datetime

def sort_by_date(data, ascending=True):
    """
    Сортирует список словарей по полю 'date' в формате YYYY-MM-DD.

    Args:
        data (list): список словарей с полем 'date'
        ascending (bool): если True — по возрастанию, иначе — по убыванию

    Returns:
        list: отсортированный список словарей
    Raises:
        ValueError: если дата имеет некорректный формат или отсутствует поле 'date'
    """
    if not data:
        return []

    def parse_date(item):
        try:
            date_str = item["date"]
            if not isinstance(date_str, str) or len(date_str) != 10:
                raise ValueError(f"Некорректный формат даты: {date_str}")
            return datetime.strptime(date_str, "%Y-%m-%d")
        except KeyError:
            raise ValueError("Отсутствует поле 'date'")
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError(f"Некорректный формат даты: {date_str}") from e
            raise

    return sorted(data, key=parse_date, reverse=not ascending)
from datetime import datetime

def sort_by_date(transactions, reverse=False):
    """
    Сортирует транзакции по дате.

    Args:
        transactions: список транзакций с полем 'date' в формате ISO
        reverse: если True — сортировка по убыванию

    Returns:
        отсортированный список транзакций
    """
    def parse_date(date_str):
        # Удаляем T и парсим до секунд
        return datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')

    return sorted(transactions, key=lambda x: parse_date(x['date']), reverse=reverse)