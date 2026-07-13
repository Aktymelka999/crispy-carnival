from decimal import Decimal
from unittest.mock import patch

from src.external_api import convert_transaction_to_rub


@patch("src.external_api.get_exchange_rate", return_value=Decimal("90.5"))
def test_convert_new_currency_format(mock_get_rate):
    tx = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}}
    result = convert_transaction_to_rub(tx)
    assert result == Decimal("9050.0")
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate", return_value=Decimal("90.5"))
def test_convert_old_currency_format_fallback(mock_get_rate):
    tx = {"operationAmount": {"amount": 100, "currency": "USD"}}
    result = convert_transaction_to_rub(tx)
    assert result == Decimal("9050.0")
    mock_get_rate.assert_called_once_with("USD", "RUB")


def test_currency_code_missing():
    tx = {"operationAmount": {"amount": 100, "currency": {}}}
    result = convert_transaction_to_rub(tx)
    assert result is None


def test_currency_none():
    tx = {"operationAmount": {"amount": 100, "currency": None}}
    result = convert_transaction_to_rub(tx)
    assert result is None


@patch("src.external_api.get_exchange_rate")
def test_rub_conversion_no_rate_needed(mock_get_rate):
    tx = {"operationAmount": {"amount": "1500.75", "currency": {"code": "RUB"}}}
    result = convert_transaction_to_rub(tx)
    assert result == Decimal("1500.75")
    mock_get_rate.assert_not_called()


def test_invalid_amount():
    tx = {"operationAmount": {"amount": "not_a_number", "currency": {"code": "USD"}}}
    result = convert_transaction_to_rub(tx)
    assert result is None


def test_missing_operation_amount():
    tx = {"amount": 100, "currency": "USD"}
    result = convert_transaction_to_rub(tx)
    assert result is None
