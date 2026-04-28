import pytest
from src.processing import sort_by_date

def test_sort_by_date_ascending():
    test_data = [
        {"state": "success", "date": "2023-01-03"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-02"},
    ]
    sorted_data = sort_by_date(test_data, ascending=True)
    dates = [item["date"] for item in sorted_data]
    expected_dates = ["2023-01-01", "2023-01-02", "2023-01-03"]
    assert dates == expected_dates, f"Ожидалось {expected_dates}, но получено {dates}"

def test_sort_by_date_descending():
    test_data = [
        {"state": "success", "date": "2023-01-03"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-02"},
    ]
    sorted_data = sort_by_date(test_data, ascending=False)
    dates = [item["date"] for item in sorted_data]
    expected_dates = ["2023-01-03", "2023-01-02", "2023-01-01"]
    assert dates == expected_dates, f"Ожидалось {expected_dates}, но получено {dates}"

def test_sort_by_date_same_dates():
    test_data = [
        {"state": "success", "date": "2023-01-01"},
        {"state": "failed", "date": "2023-01-01"},
        {"state": "pending", "date": "2023-01-01"},
    ]
    sorted_data = sort_by_date(test_data, ascending=True)
    dates = [item["date"] for item in sorted_data]
    assert all(date == "2023-01-01" for date in dates), "Все даты должны быть '2023-01-01'"

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
    with pytest.raises(ValueError) as exc_info:
        sort_by_date(test_data, ascending=True)

    error_msg = str(exc_info.value)
    assert any(msg in error_msg for msg in [
        "Некорректный формат даты",
        "Отсутствует поле 'date'"
    ]), f"Ошибка должна содержать сообщение о проблеме с датой, но получила: {error_msg}"