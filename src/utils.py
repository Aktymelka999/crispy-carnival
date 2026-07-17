import re
from collections import Counter
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


def get_currency_code(tx: Dict[str, Any]) -> Optional[str]:
    if "currency" in tx and isinstance(tx["currency"], str):
        return tx["currency"].upper()

    op_amount = tx.get("operationAmount")
    if isinstance(op_amount, dict):
        curr = op_amount.get("currency")
        if isinstance(curr, dict):
            code = curr.get("code")
            if code:
                return str(code).upper()
            name = curr.get("name", "")
            if isinstance(name, str) and "руб" in name.lower():
                return "RUB"
    return None


def get_amount_decimal(tx: Dict[str, Any]) -> Decimal:
    amount = tx.get("amount")
    if amount is not None:
        try:
            return Decimal(str(amount))
        except InvalidOperation, ValueError, TypeError:
            pass

    op_amount = tx.get("operationAmount")
    if isinstance(op_amount, dict):
        amount_val = op_amount.get("amount")
        if amount_val is not None:
            try:
                return Decimal(str(amount_val))
            except InvalidOperation, ValueError, TypeError:
                pass
    return Decimal("0")


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    if not search:
        return data

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result: List[Dict[str, Any]] = []

    for operation in data:
        description = operation.get("description")
        if isinstance(description, str) and pattern.search(description):
            result.append(operation)
    return result


def count_operations_by_categories(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    filtered_categories = [op.get("category") for op in data if op.get("category") in categories]
    counter = Counter(filtered_categories)
    return {cat: counter.get(cat, 0) for cat in categories}
