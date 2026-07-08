from unittest.mock import patch
from src.external_api import convert_transaction_amount, get_exchange_rate
from decimal import Decimal

@patch("src.external_api.requests.get")
def test_convert_transaction_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "rates": {"RUB": 90.5},
        "base": "USD"
    }
    mock_response.raise_for_status.return_value = None

    tx = {"amount": 100, "currency": "USD", "target_currency": "RUB"}
    result = convert_transaction_amount(tx)

    assert result is not None
    assert result == Decimal("9050.00")  # 100 * 90.5

@patch("src.external_api.requests.get")
def test_get_exchange_rate_missing_key(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"rates": {}, "base": "USD"}
    mock_response.raise_for_status.return_value = None

    rate = get_exchange_rate("USD", "RUB")
    assert rate is None
