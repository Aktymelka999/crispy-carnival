import pytest
import sys
from pathlib import Path
from decimal import Decimal

project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import (
    process_bank_search,
    count_operations_by_categories,
    get_currency_code,
    get_amount_decimal,
)


class TestProcessBankSearch:
    def test_found_exact_match(self):
        data = [
            {"id": 1, "description": "Оплата в магазине Пятёрочка"},
            {"id": 2, "description": "Перевод другу"},
        ]
        res = process_bank_search(data, "Пятёрочка")
        assert len(res) == 1
        assert res[0]["id"] == 1

    def test_case_insensitive(self):
        data = [{"id": 3, "description": "ОПЛАТА В СУПЕРМАРКЕТЕ"}]
        assert len(process_bank_search(data, "оплата")) == 1

    def test_special_chars(self):
        data = [{"id": 4, "description": "Платёж 100$"}]
        assert len(process_bank_search(data, "$")) == 1

    def test_empty_search_returns_all(self):
        data = [{"id": 5, "description": "Любая операция"}]
        res = process_bank_search(data, "")
        assert len(res) == 1
        assert res[0]["id"] == 5

    def test_missing_or_invalid_description(self):
        data = [
            {"id": 6},
            {"id": 7, "description": None},
            {"id": 8, "description": 123},
        ]
        assert process_bank_search(data, "что-то") == []


class TestCountOperationsByCategories:
    def test_count_categories(self):
        data = [
            {"category": "groceries"},
            {"category": "groceries"},
            {"category": "transfers"},
            {"category": "online"},
        ]
        cats = ["groceries", "transfers", "online", "other"]
        res = count_operations_by_categories(data, cats)
        assert res == {"groceries": 2, "transfers": 1, "online": 1, "other": 0}

    def test_empty_data(self):
        data = []
        cats = ["groceries", "other"]
        res = count_operations_by_categories(data, cats)
        assert res == {"groceries": 0, "other": 0}


class TestGetCurrencyCode:
    def test_flat_currency(self):
        tx = {"currency": "usd"}
        assert get_currency_code(tx) == "USD"

    def test_nested_currency_code(self):
        tx = {"operationAmount": {"currency": {"code": "eur"}}}
        assert get_currency_code(tx) == "EUR"

    def test_nested_currency_name_fallback(self):
        tx = {"operationAmount": {"currency": {"name": "Российский рубль"}}}
        assert get_currency_code(tx) == "RUB"

    def test_no_currency_field(self):
        tx = {"amount": 100}
        assert get_currency_code(tx) is None


class TestGetAmountDecimal:
    def test_flat_amount(self):
        tx = {"amount": 123.45}
        assert get_amount_decimal(tx) == Decimal("123.45")

    def test_nested_amount(self):
        tx = {"operationAmount": {"amount": 99.99}}
        assert get_amount_decimal(tx) == Decimal("99.99")

    def test_invalid_amount_fallback(self):
        tx = {"amount": "invalid", "operationAmount": {"amount": 50}}
        assert get_amount_decimal(tx) == Decimal("50")

    def test_zero_fallback(self):
        tx = {"amount": None}
        assert get_amount_decimal(tx) == Decimal("0")
