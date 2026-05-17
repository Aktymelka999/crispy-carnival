import sys
import os

# Получаем путь к директории tests
tests_dir = os.path.dirname(__file__)
# Поднимаемся на уровень вверх (к корневой директории проекта) и добавляем src
src_path = os.path.abspath(os.path.join(tests_dir, '../src'))
# Добавляем путь в начало sys.path
if src_path not in sys.path:
    sys.path.insert(0, src_path)


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

import pytest

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 594224789,
            "state": "EXECUTED",
            "date": "2019-05-19T08:26:52.132456",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "RUB",
                    "code": "RUB"
                }
            },
            "description": "Оплата товара",
            "from": "Счет 44364709524079543610",
            "to": "Счет 79334689482157544633"
        }
    ]

@pytest.fixture
def empty_transactions():
    """Фикстура для пустого списка транзакций."""
    return []