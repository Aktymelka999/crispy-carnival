from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_transaction_to_rub, get_exchange_rate


@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get):
    # 1. Настраиваем мок-ответ от API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}  # 1 USD = 90.5 RUB
    mock_get.return_value = mock_response

    # 2. Данные транзакции
    transaction = {"amount": 100, "currency": "USD"}

    # 3. Вызываем функцию
    result = convert_transaction_to_rub(transaction)

    # 4. Проверяем результат
    assert result == 9050.0  # 100 * 90.5

    # 5. Проверяем, что запрос был сделан с правильными параметрами
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert "USD" in str(call_args)  # Проверка, что base=USD
    assert "RUB" in str(call_args)  # Проверка, что symbols=RUB


@patch("src.external_api.requests.get")
def test_convert_eur_to_rub(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 98.2}}
    mock_get.return_value = mock_response

    transaction = {"amount": 50, "currency": "EUR"}
    result = convert_transaction_to_rub(transaction)

    assert result == 4910.0  # 50 * 98.2


def test_convert_rub_no_api_call():
    """
    Тест, который проверяет, что для RUB API вообще не вызывается.

    """
    transaction = {"amount": 1500, "currency": "RUB"}

    # Используем patch для requests.get, но ожидаем, что он НЕ будет вызван
    with patch("src.external_api.requests.get") as mock_get:
        result = convert_transaction_to_rub(transaction)
        assert result == 1500.0
        mock_get.assert_not_called()


@patch("src.external_api.requests.get")
def test_api_error_handling(mock_get):
    # Имитируем ошибку сети или 404 от API
    mock_get.side_effect = Exception("Network error")

    transaction = {"amount": 100, "currency": "USD"}

    # Функция должна пробросить ошибку дальше
    with pytest.raises(Exception):
        convert_transaction_to_rub(transaction)
