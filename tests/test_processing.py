from typing import List, Dict, Any
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_valid() -> None:
    data: List[Dict[str, Any]] = [
        {"id": 1, "state": "COMPLETED", "amount": 100},
        {"id": 2, "state": "PENDING", "amount": 200},
        {"id": 3, "state": "COMPLETED", "amount": 300},
    ]
    result = filter_by_state(data, "COMPLETED")
    assert len(result) == 2
    assert all(item["state"] == "COMPLETED" for item in result)


def test_filter_by_state_empty_list() -> None:
    data: List[Dict[str, Any]] = []
    result = filter_by_state(data, "COMPLETED")
    assert result == []


def test_filter_by_state_no_matching_state() -> None:
    data: List[Dict[str, Any]] = [
        {"id": 1, "state": "PENDING", "amount": 100},
        {"id": 2, "state": "FAILED", "amount": 200},
    ]
    result = filter_by_state(data, "COMPLETED")
    assert result == []


def test_sort_by_date_valid_ascending() -> None:
    data: List[Dict[str, Any]] = [
        {"id": 1, "date": "2024-01-01", "amount": 100},
        {"id": 2, "date": "2023-12-31", "amount": 200},
        {"id": 3, "date": "2024-02-01", "amount": 300},
    ]
    result = sort_by_date(data)
    assert result[0]["id"] == 2  # 2023-12-31
    assert result[1]["id"] == 1  # 2024-01-01
    assert result[2]["id"] == 3  # 2024-02-01


def test_sort_by_date_empty_list() -> None:
    data: List[Dict[str, Any]] = []
    result = sort_by_date(data)
    assert result == []


def test_sort_by_date_single_item() -> None:
    data: List[Dict[str, Any]] = [{"id": 1, "date": "2024-05-01", "amount": 500}]
    result = sort_by_date(data)
    assert len(result) == 1
    assert result[0]["id"] == 1
