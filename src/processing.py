import logging
from typing import Any, Dict, List

logger = logging.getLogger("src.processing")


def filter_by_state(
    transactions: List[Dict[str, Any]],
    state: str,
) -> List[Dict[str, Any]]:
    if not isinstance(transactions, list):
        logger.warning("filter_by_state: передан не список, возвращаем пустой список")
        return []

    result = [t for t in transactions if isinstance(t, dict) and t.get("state") == state]
    logger.info("Отфильтровано %d транзакций по state=%s", len(result), state)
    return result


def sort_by_date(
    transactions: List[Dict[str, Any]],
    reverse: bool = False,
) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по полю date (строка в формате YYYY-MM-DD).
    Элементы без валидного поля date сортируются в начало (при reverse=False).
    """
    if not isinstance(transactions, list):
        logger.warning("sort_by_date: передан не список, возвращаем пустой список")
        return []

    def get_date_key(txn: Dict[str, Any]) -> str:
        val = txn.get("date")
        if isinstance(val, str):
            return val
        return ""

    try:
        result = sorted(transactions, key=get_date_key, reverse=reverse)
        logger.info(
            "Отсортировано %d транзакций, reverse=%s",
            len(result),
            reverse,
        )
        return result
    except Exception as e:
        logger.exception("Ошибка при сортировке транзакций: %s", e)
        return []
