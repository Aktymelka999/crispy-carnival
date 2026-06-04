import pytest
from src.generators import (
    filter_by_currency,
    description_generator,
    card_number_generator,
    transaction_descriptions 
)
# Фикстура с тестовыми данными
@pytest.fixture
def transactions():
    return [
        {"id": 1, "operationAmount": {"currency": "USD", "amount": 100}},
        {"id": 2, "operationAmount": {"currency": "EUR", "amount": 200}},
        {"id": 3, "operationAmount": {"currency": "USD", "amount": 150}},
        {"id": 4, "operationAmount": {"currency": "RUB", "amount": 5000}},
        {"id": 5, "operationAmount": {"currency": "USD", "amount": 200}}
    ]

# Тест 1: базовая фильтрация по валюте
def test_filter_by_currency_basic(transactions):
    usd_transactions = list(filter_by_currency(transactions, "USD"))
    assert len(usd_transactions) == 3
    for tx in usd_transactions:
        assert tx['operationAmount']['currency'] == "USD"


# Тест 2: фильтрация по несуществующей валюте 
def test_filter_by_currency_nonexistent(transactions):
    nonexistent_currency = list(filter_by_currency(transactions, "JPY"))
    assert len(nonexistent_currency) == 0

# Тест 3: пустой список транзакций
def test_filter_by_currency_empty_list():
    empty_transactions = []
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert len(result) == 0

# Тест 4: одна транзакция, совпадающая с фильтром
def test_filter_by_currency_single_match():
    single_tx = [
        {
            "id": 1,
            "operationAmount": {"currency": "EUR", "amount": 100}
        }
    ]
    result = list(filter_by_currency(single_tx, "EUR"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"] == "EUR"

# Тест 5: одна транзакция, не совпадающая с фильтром 
def test_filter_by_currency_single_no_match():
    single_tx = [{"id": 1, "currency": "EUR", "amount": 100}]
    result = list(filter_by_currency(single_tx, "USD"))
    assert len(result) == 0

# Тест 6: проверка итератора (что функция действительно возвращает итератор)
def test_filter_by_currency_iterator(transactions):
    iterator = filter_by_currency(transactions, "USD")
    assert hasattr(iterator, '__iter__')
    assert hasattr(iterator, '__next__')

# Тест 7: чувствительность к регистру (если функция не должна быть регистрозависимой)
def test_filter_by_currency_case_insensitive(transactions):
    usd_lower = list(filter_by_currency(transactions, "usd"))
    usd_upper = list(filter_by_currency(transactions, "USD"))
    assert usd_lower == usd_upper

# Тест 8: проверка на устойчивость к None в списке транзакций
def test_filter_by_currency_none_values():
    transactions_with_none = [
        None,
        {
            "id": 1,
            "operationAmount": {"currency": "USD", "amount": 100}
        },
        None
    ]
    result = list(filter_by_currency(transactions_with_none, "USD"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"] == "USD"

# Тест 9: проверка на отсутствие ключа 'currency' в словаре
def test_filter_by_currency_missing_key():
    transactions_missing_key = [
        {"id": 1, "amount": 100},  # Нет поля operationAmount
        {
            "id": 2,
            "operationAmount": {"currency": "USD", "amount": 200}
        }
    ]
    result = list(filter_by_currency(transactions_missing_key, "USD"))
    assert len(result) == 1
    assert result[0]["operationAmount"]["currency"] == "USD"

    
def test_filter_by_currency_invalid_input_type():
    with pytest.raises(TypeError):
        list(filter_by_currency("not a list", "USD"))
    with pytest.raises(TypeError):
        list(filter_by_currency({"key": "value"}, "USD"))

def test_filter_by_currency_invalid_operation_amount():
    transactions = [
        {"id": 1, "operationAmount": "not a dict"},
        {"id": 2, "operationAmount": None},
        {"id": 3, "operationAmount": 123}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_currency_in_operation_amount():
    transactions = [
        {"id": 1, "operationAmount": {"amount": 100}},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"other_field": "value"}}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_mixed_case():
    transactions = [
        {"id": 1, "operationAmount": {"currency": "UsD", "amount": 100}},
        {"id": 2, "operationAmount": {"currency": "uSd", "amount": 200}}
    ]
    result = list(filter_by_currency(transactions, "usd"))
    assert len(result) == 2

def test_filter_by_currency_edge_cases_currency():
    # Пустая строка
    result_empty = list(filter_by_currency([], ""))
    assert len(result_empty) == 0

    # None в качестве валюты (если допустимо)
    result_none = list(filter_by_currency([], None))
    assert len(result_none) == 0
    
def test_filter_by_currency_invalid_input_type():
    with pytest.raises(TypeError):
        list(filter_by_currency("not a list", "USD"))
    with pytest.raises(TypeError):
        list(filter_by_currency(123, "USD"))
    with pytest.raises(TypeError):
        list(filter_by_currency({"key": "value"}, "USD"))

def test_filter_by_currency_invalid_operation_amount():
    transactions = [
        {"id": 1, "operationAmount": "not a dict"},
        {"id": 2, "operationAmount": None},
        {"id": 3, "operationAmount": 123}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_missing_currency_in_operation_amount():
    transactions = [
        {"id": 1, "operationAmount": {"amount": 100}},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"other_field": "value"}}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 0

def test_filter_by_currency_skip_none_and_non_dict():
    transactions = [
        None,
        "not a transaction",
        123,
        {"id": 1, "operationAmount": {"currency": "USD", "amount": 100}}
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 1
    assert result[0]["id"] == 1

def test_filter_by_currency_edge_cases_currency():
    # Пустая строка
    result_empty = list(filter_by_currency([], ""))
    assert len(result_empty) == 0

    # None в качестве валюты (если допустимо)
    result_none = list(filter_by_currency([], None))
    assert len(result_none) == 0

    import pytest

def test_description_generator_with_description():
    transactions = [
        {"id": 1, "description": "Покупка в магазине"},
        {"id": 2, "description": "Перевод другу"}
    ]
    result = list(description_generator(transactions))
    assert result == ["Покупка в магазине", "Перевод другу"]

def test_description_generator_without_description():
    transactions = [
        {"id": 1},
        {"id": 2, "amount": 100}
    ]
    result = list(description_generator(transactions))
    assert result == ["Описание отсутствует", "Описание отсутствует"]

def test_description_generator_mixed():
    transactions = [
        {"id": 1, "description": "Оплата услуг"},
        {"id": 2},  # без описания
        {"id": 3, "description": "Возврат средств"}
    ]
    result = list(description_generator(transactions))
    assert result == ["Оплата услуг", "Описание отсутствует", "Возврат средств"]

def test_card_number_generator_normal_range():
    result = list(card_number_generator(123456789012345, 123456789012347))
    expected = [
        "0123456789012345",
        "0123456789012346",
        "0123456789012347"
    ]
    assert result == expected

def test_card_number_generator_single_number():
    result = list(card_number_generator(1000, 1000))
    assert result == ["0000000000001000"]

def test_card_number_generator_empty_range():
    result = list(card_number_generator(100, 99))
    assert result == []

def test_card_number_generator_leading_zeros():
    result = list(card_number_generator(1, 3))
    expected = ["0000000000000001", "0000000000000002", "0000000000000003"]
    assert result == expected

def test_card_number_generator_large_numbers():
    result = list(card_number_generator(9999999999999998, 9999999999999999))
    expected = [
        "9999999999999998",
        "9999999999999999"
    ]
    assert result == expected

def test_transaction_descriptions_with_descriptions():
    """Тест: все транзакции содержат поле description."""
    transactions = [
        {"id": 1, "description": "Перевод со счета на счет"},
        {"id": 2, "description": "Покупка в магазине"},
        {"id": 3, "description": "Оплата услуг ЖКХ"}
    ]
    result = list(transaction_descriptions(transactions))
    expected = ["Перевод со счета на счет", "Покупка в магазине", "Оплата услуг ЖКХ"]
    assert result == expected


def test_transaction_descriptions_without_descriptions():
    """Тест: ни одна транзакция не содержит поле description."""
    transactions = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200, "currency": "RUB"},
        {"id": 3}
    ]
    result = list(transaction_descriptions(transactions))
    expected = ["Описание отсутствует", "Описание отсутствует", "Описание отсутствует"]
    assert result == expected

def test_transaction_descriptions_mixed():
    """Тест: смешанный случай — некоторые транзакции имеют description, некоторые нет."""
    transactions = [
        {"id": 1, "description": "Перевод другу"},
        {"id": 2},  # без описания
        {"id": 3, "description": "Оплата интернета"},
        {"id": 4, "amount": 500}  # без описания
    ]
    result = list(transaction_descriptions(transactions))
    expected = [
        "Перевод другу",
        "Описание отсутствует",
        "Оплата интернета",
        "Описание отсутствует"
    ]
    assert result == expected

def test_transaction_descriptions_empty_list():
    """Тест: пустой список транзакций."""
    transactions = []
    result = list(transaction_descriptions(transactions))
    assert result == []

def test_transaction_descriptions_single_transaction_with_description():
    """Тест: одна транзакция с описанием."""
    transactions = [{"id": 1, "description": "Единственный перевод"}]
    result = list(transaction_descriptions(transactions))
    assert result == ["Единственный перевод"]

def test_transaction_descriptions_single_transaction_without_description():
    """Тест: одна транзакция без описания."""
    transactions = [{"id": 1}]
    result = list(transaction_descriptions(transactions))
    assert result == ["Описание отсутствует"]

def test_transaction_descriptions_none_input():
    """Тест: входное значение None."""
    with pytest.raises(TypeError):
        list(transaction_descriptions(None))

def test_transaction_descriptions_non_iterable_input():
    """Тест: неитерируемый входной параметр (число)."""
    with pytest.raises(TypeError):
        list(transaction_descriptions(123))

def test_transaction_descriptions_list_with_non_dict_elements():
    """Тест: список содержит не словари."""
    transactions = ["не словарь", 123, None]
    with pytest.raises(KeyError):
        list(transaction_descriptions(transactions))

def test_transaction_descriptions_generator_behavior():
    """Тест: проверка ленивой загрузки (генератора)."""
    transactions = [
        {"id": 1, "description": "Первая транзакция"},
        {"id": 2, "description": "Вторая транзакция"}
    ]
    generator = transaction_descriptions(transactions)
    first = next(generator)
    second = next(generator)
    assert first == "Первая транзакция"
    assert second == "Вторая транзакция"

    #card_number_generator
    import pytest

def test_card_number_generator_normal_range():
    """Тест: нормальный диапазон номеров карт (16‑значные)."""
    result = list(card_number_generator(1234567890123456, 1234567890123458))
    expected = [
        "1234567890123456",
        "1234567890123457",
        "1234567890123458"
    ]
    assert result == expected

def test_card_number_generator_single_number():
    """Тест: генерация одного номера карты."""
    result = list(card_number_generator(4111111111111111, 4111111111111111))
    assert result == ["4111111111111111"]

def test_card_number_generator_empty_range():
    """Тест: пустой диапазон (start > end)."""
    result = list(card_number_generator(1000, 999))
    assert result == []

def test_card_number_generator_leading_zeros():
    """Тест: номера с ведущими нулями (дополнение до 16 цифр)."""
    result = list(card_number_generator(1, 3))
    expected = ["0000000000000001", "0000000000000002", "0000000000000003"]
    assert result == expected

def test_card_number_generator_large_numbers():
    """Тест: очень большие номера карт."""
    result = list(card_number_generator(9999999999999998, 9999999999999999))
    expected = ["9999999999999998", "9999999999999999"]
    assert result == expected

def test_card_number_generator_boundary_values():
    """Тест: граничные значения (минимальный и максимальный 16‑значный номер)."""
    result = list(card_number_generator(0, 1))
    expected = ["0000000000000000", "0000000000000001"]
    assert result == expected

def test_card_number_generator_generator_behavior():
    """Тест: проверка ленивой загрузки (генератора)."""
    generator = card_number_generator(5555555555554444, 5555555555554446)
    first = next(generator)
    second = next(generator)
    third = next(generator)
    assert first == "5555555555554444"
    assert second == "5555555555554445"
    assert third == "5555555555554446"

def test_card_number_generator_negative_numbers():
    """Тест: отрицательные номера карт (должны быть обработаны корректно)."""
    with pytest.raises(ValueError):
        list(card_number_generator(-1, 1))

def test_card_number_generator_invalid_types():
    """Тест: некорректные типы входных данных."""
    with pytest.raises(TypeError):
        list(card_number_generator("123", "456"))
    with pytest.raises(TypeError):
        list(card_number_generator(None, 1000))

def test_card_number_generator_large_range():
    """Тест: большой диапазон номеров (проверка производительности и корректности)."""
    result = list(card_number_generator(1000000000000000, 1000000000000002))
    expected = [
        "1000000000000000",
        "1000000000000001",
        "1000000000000002"
    ]
    assert result == expected