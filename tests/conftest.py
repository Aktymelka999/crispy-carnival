from datetime import datetime

import pytest


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": "txn_001",
            "amount": 1500.50,
            "currency": "RUB",
            "type": "DEBIT",
            "timestamp": datetime(2024, 6, 1, 10, 30, 0),
            "description": "Оплата услуг",
            "state": "EXECUTED",
            "date": "2024-06-01",
        },
        {
            "id": "txn_002",
            "amount": -300.00,
            "currency": "RUB",
            "type": "CREDIT",
            "timestamp": datetime(2024, 6, 2, 9, 15, 0),
            "description": "Возврат средств",
            "state": "PENDING",
            "date": "2024-06-02",
        },
        {
            "id": "txn_003",
            "amount": 5000.00,
            "currency": "USD",
            "type": "DEBIT",
            "timestamp": datetime(2024, 6, 3, 14, 20, 0),
            "description": "Покупка валюты",
            "state": "EXECUTED",
            "date": "2024-06-03",
        },
    ]
