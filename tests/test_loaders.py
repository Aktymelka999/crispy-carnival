import os
import tempfile

import pandas as pd
import pytest

from src.loaders import load_transactions_from_file


@pytest.fixture
def csv_file_path():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8", newline="") as f:
        csv_content = """id,amount,currency,type,state,date,description
txn_001,1500.50,RUB,DEBIT,EXECUTED,2024-06-01,Оплата услуг
txn_002,-300.00,RUB,CREDIT,PENDING,2024-06-02,Возврат средств
txn_003,5000.00,USD,DEBIT,EXECUTED,2024-06-03,Покупка валюты
"""
        f.write(csv_content)
        path = f.name
    yield path
    os.unlink(path)


@pytest.fixture
def xlsx_file_path():
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        path = f.name

    data = {
        "id": ["txn_004", "txn_005"],
        "amount": [2000.0, -100.0],
        "currency": ["RUB", "EUR"],
        "type": ["DEBIT", "CREDIT"],
        "state": ["EXECUTED", "PENDING"],
        "date": ["2024-07-01", "2024-07-02"],
        "description": ["Перевод другу", "Списание комиссии"],
    }
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    yield path
    os.unlink(path)


def test_load_csv(csv_file_path):
    transactions = load_transactions_from_file(csv_file_path)
    assert len(transactions) == 3
    assert transactions[0]["id"] == "txn_001"
    assert transactions[0]["state"] == "EXECUTED"


def test_load_xlsx(xlsx_file_path):
    transactions = load_transactions_from_file(xlsx_file_path)
    assert len(transactions) == 2
    assert transactions[0]["id"] == "txn_004"


def test_load_invalid_format():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        dummy_path = f.name
    try:
        with pytest.raises(ValueError):
            load_transactions_from_file(dummy_path)
    finally:
        os.unlink(dummy_path)


def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_transactions_from_file("nonexistent.csv")
