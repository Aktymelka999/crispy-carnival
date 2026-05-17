import pytest
from src.generators.data_generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator
)
from typing import List, Dict, Any

@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            'date': '2018-06-30T02:08:58.425572',
            'description': 'Перевод организации',
            'from': 'Счёт 75106830613657916952',
            'id': 939719570,
            'operationAmount': {
                'amount': '31957.58',
                'currency': {'name': 'RUB', 'code': '643'}
            }
        },
        {
            'date': '2019-05-19T08:26:52.132456',
            'description': 'Оплата товара',
            'from': 'Счёт 44364709524079543610',
            'id': 594224789,
            'operationAmount': {
                'amount': '100',
                'currency': {'name': 'USD', 'code': '840'}
            }
        },
        {
            'date': '2020-01-01T12:00:00.000000',
            'description': 'Покупка в магазине',
            'id': 123456789,
            'operationAmount': {
                'amount': '50',
                'currency': {'name': 'USD', 'code': '840'}
            }
        }
    ]

@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    return []

class TestFilterByCurrency:

    def test_filter_usd_transactions(self, sample_transactions: ListDict[str, Any]) -> None:
        """Тест фильтрации транзакций в USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 2

    def test_filter_rub_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации транзакций в RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 1

    def test_no_matching_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест когда нет транзакций в заданной валюте."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_empty_transactions_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Тест с пустым списком транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_transaction_without_operation_amount(self) -> None:
        """Тест транзакции без поля operationAmount."""
        transactions = [
            {"id": 1, "description": "Без суммы"},
            {"id": 2, "operationAmount": {"amount": "100", "currency": {"name": "USD"}}}
        ]
        usd_transactions = list(filter_by_currency(transactions, "USD"))
        assert len(usd_transactions) == 1

    @pytest.mark.parametrize("currency,expected_count", [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0)
    ])
    def test_parametrized_filtering(
        self,
        sample_transactions: List[Dict[str, Any]],
        currency: str,
        expected_count: int
    ) -> None:
        """Параметризованный тест фильтрации по разным валютам."""
        filtered = list(filter_by_currency(sample_transactions, currency))
        assert len(filtered) == expected_count

class TestTransactionDescriptions:

    def test_get_all_descriptions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест получения всех описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))
        assert len(descriptions) == 3
        assert "Перевод организации" in descriptions
        assert "Оплата товара" in descriptions

    def test_empty_transactions_list(self, empty_transactions: List[Dict[str, Any]]) -> None:
        """Тест с пустым списком транзакций."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert descriptions == []
