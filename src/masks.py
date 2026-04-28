def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты по шаблону: XXXX XX** **** XXXX"""
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать ровно 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счёта по шаблону: **XXXX (только последние 4 цифры)"""
    if len(account_number) != 20 or not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать ровно 20 цифр")
    return f"**{account_number[-4:]}"

import pytest
from .processing import sort_by_date  

def test_sort_by_date_ascending():
    test_data = [
        {"state": "success", "date": "2023-01-03"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-02"},
    ]
    sorted_data = sort_by_date(test_data, ascending=True)
    dates = [item["date"] for item in sorted_data]
    assert dates == ["2023-01-01", "2023-01-02", "2023-01-03"]

def test_sort_by_date_descending():
    test_data = [
        {"state": "success", "date": "2023-01-03"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-02"},
    ]
    sorted_data = sort_by_date(test_data, ascending=False)
    dates = [item["date"] for item in sorted_data]
    assert dates == ["2023-01-03", "2023-01-02", "2023-01-01"]

def test_sort_by_date_same_dates():
    test_data = [
        {"state": "success", "date": "2023-01-01"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-01"},
    ]
    sorted_data = sort_by_date(test_data, ascending=True)
    dates = [item["date"] for item in sorted_data]
    assert all(date == "2023-01-01" for date in dates)

@pytest.mark.parametrize("invalid_date_data", [
    {"state": "success", "date": "invalid_date"},
    {"state": "failed", "date": "32.01.2023"},
    {"state": "pending", "date": None},
])
def test_sort_by_date_invalid_formats(invalid_date_data):
    test_data = [
        {"state": "success", "date": "2023-01-01"},
        invalid_date_data,
        {"state": "pending", "date": "2023-01-02"},
    ]
    with pytest.raises(ValueError):
        sort_by_date(test_data, ascending=True)