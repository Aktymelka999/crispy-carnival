from decimal import Decimal, InvalidOperation
from typing import Any, Optional


def get_currency_code(tx: dict[str, Any]) -> Optional[str]:
    """
    Извлекает код валюты из транзакции.
    Поддерживает оба формата:
      - плоский: {"currency": "RUB"}
      - вложенный: {"operationAmount": {"currency": {"code": "RUB"}}}
    Возвращает код в верхнем регистре или None.
    """

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


def get_amount_decimal(tx: dict[str, Any]) -> Decimal:
    """
    Безопасное извлечение суммы как Decimal.
    Поддерживает вложенный формат operationAmount.amount.
    Если не получилось распарсить — возвращает 0.
    """
    amount = tx.get("amount")
    if amount is not None:
        try:
            return Decimal(str(amount))
        except InvalidOperation:
            pass

    op_amount = tx.get("operationAmount")
    if isinstance(op_amount, dict):
        amount_val = op_amount.get("amount")
        if amount_val is not None:
            try:
                return Decimal(str(amount_val))
            except InvalidOperation:
                pass

    return Decimal("0")
