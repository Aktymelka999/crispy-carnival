
from src.generators import (
    filter_by_currency,
    card_number_generator,
    description_generator,
    transaction_descriptions,
)

# --- Тесты для filter_by_currency ---


def test_filter_by_currency_basic():
    data = [
        {"id": 1, "currency": "RUB", "amount": 100},
        {"id": 2, "currency": "USD", "amount": 200},
        {"id": 3, "currency": "RUB", "amount": 300},
    ]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 2
    assert all(t["currency"] == "RUB" for t in result)
    assert {t["id"] for t in result} == {1, 3}


def test_filter_by_currency_nonexistent():
    data = [
        {"id": 1, "currency": "EUR", "amount": 100},
        {"id": 2, "currency": "JPY", "amount": 200},
    ]
    assert filter_by_currency(data, "RUB") == []


def test_filter_by_currency_empty_list():
    assert filter_by_currency([], "RUB") == []


def test_filter_by_currency_single_match():
    data = [{"id": 1, "currency": "RUB", "amount": 100}]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_currency_single_no_match():
    data = [{"id": 1, "currency": "USD", "amount": 100}]
    assert filter_by_currency(data, "RUB") == []


def test_filter_by_currency_iterator_input():
    # Генератор не является списком, поэтому функция вернёт []
    data_gen = ({"id": i, "currency": "RUB" if i % 2 == 0 else "USD", "amount": i} for i in range(5))
    assert filter_by_currency(data_gen, "RUB") == []


def test_filter_by_currency_case_sensitive():
    data = [
        {"id": 1, "currency": "rub"},
        {"id": 2, "currency": "RUB"},
        {"id": 3, "currency": "Rub"},
    ]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 1
    assert result[0]["currency"] == "RUB"


def test_filter_by_currency_none_values():
    data = [None, {"id": 1, "currency": "RUB"}, None]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_currency_missing_key():
    data = [
        {"id": 1},  # нет currency
        {"id": 2, "currency": "RUB"},
        {"id": 3},  # нет currency
    ]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_currency_invalid_input_type():
    assert filter_by_currency("not a list", "RUB") == []
    assert filter_by_currency(123, "RUB") == []
    assert filter_by_currency(None, "RUB") == []


def test_filter_by_currency_mixed_case_and_types():
    data = [
        None,
        "string",
        123,
        {"id": 1, "currency": "RUB"},
        {"id": 2},
        {"id": 3, "currency": "rub"},
    ]
    result = filter_by_currency(data, "RUB")
    assert len(result) == 1
    assert result[0]["id"] == 1


# --- Тесты для card_number_generator ---


def test_card_number_generator_basic():
    numbers = card_number_generator(16, 5)
    assert isinstance(numbers, list)
    assert len(numbers) == 5
    assert all(isinstance(n, str) and len(n) == 16 for n in numbers)
    # Убедимся, что все номера состоят только из цифр
    assert all(n.isdigit() for n in numbers)


def test_card_number_generator_zero_count():
    assert card_number_generator(16, 0) == []


def test_card_number_generator_negative_count():
    assert card_number_generator(16, -3) == []


def test_card_number_generator_invalid_length():
    assert card_number_generator(-1, 5) == []
    assert card_number_generator(0, 5) == []


def test_card_number_generator_different_lengths():
    for length in [8, 13, 16, 19]:
        numbers = card_number_generator(length, 3)
        assert len(numbers) == 3
        assert all(len(n) == length and n.isdigit() for n in numbers)


def test_card_number_generator_uniqueness_not_required():

    numbers = card_number_generator(4, 100)

    assert len(numbers) == 100
    assert all(len(n) == 4 and n.isdigit() for n in numbers)


def test_description_generator_positive_count():
    descriptions = description_generator(5)
    assert isinstance(descriptions, list)
    assert len(descriptions) == 5
    assert all(isinstance(d, str) and len(d) > 0 for d in descriptions)

    assert any("#" in d for d in descriptions)


def test_description_generator_zero_and_negative():
    assert description_generator(0) == []
    assert description_generator(-5) == []


def test_description_generator_large_count():
    # Проверка, что функция не падает при большом количестве
    descriptions = description_generator(1000)
    assert len(descriptions) == 1000
    assert all("#" in d for d in descriptions[:10])


def test_transaction_descriptions_basic():
    descriptions = transaction_descriptions(3)
    assert isinstance(descriptions, list)
    assert len(descriptions) == 3
    assert all(isinstance(d, str) for d in descriptions)


def test_transaction_descriptions_zero():
    assert transaction_descriptions(0) == []


def test_transaction_descriptions_matches_description_generator():
    assert transaction_descriptions(5) == description_generator(5)
