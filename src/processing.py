import re
from collections import Counter
from typing import List, Dict, Any

from src.utils import get_currency_code

AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def filter_by_state(transactions: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу (state/status), регистронезависимо."""
    status_upper = status.upper()
    result = []
    for tx in transactions:
        state = tx.get("state") or tx.get("status") or ""
        if state.upper() == status_upper:
            result.append(tx)
    return result


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> List[Dict[str, Any]]:
    code = currency_code.upper()
    return [tx for tx in transactions if get_currency_code(tx) == code]


def sort_by_date(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортирует по дате. Поддерживает ISO-строки вида YYYY-MM-DDT..."""

    def key_date(tx: Dict[str, Any]) -> str:
        d = tx.get("date", "")
        if not isinstance(d, str):
            return ""
        # ISO-строка сортируется лексикографически корректно
        return d

    return sorted(transactions, key=key_date)


def process_bank_search(transactions: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Ищет по описанию с помощью regex (регистронезависимо)."""
    if not search_term.strip():
        return transactions
    pattern = re.compile(re.escape(search_term), flags=re.IGNORECASE)
    result = []
    for tx in transactions:
        desc = str(tx.get("description", ""))
        if pattern.search(desc):
            result.append(tx)
    return result


def count_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    patterns = {cat: re.compile(re.escape(cat), flags=re.IGNORECASE) for cat in categories}
    counter: Counter[str] = Counter()
    for tx in transactions:
        description = str(tx.get("description", ""))
        for category, pattern in patterns.items():
            if pattern.search(description):
                counter[category] += 1
    return dict(counter)
