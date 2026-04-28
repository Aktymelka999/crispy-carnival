import pytest
from datetime import datetime

@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00",
            "description": "Перевод"
        },
        {
            "id": 2,
            "state": "PENDING",
            "date": "2023-01-02T13:00:00",
            "description": "Оплата"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-01-03T14:00:00",
            "description": "Снятие"
        }
    ]