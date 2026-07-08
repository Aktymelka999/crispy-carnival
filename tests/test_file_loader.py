from pathlib import Path
import pytest
from src.file_loader import load_transactions
from decimal import Decimal

def test_load_transactions_exists(tmp_path):
    test_file = tmp_path / "ops.json"
    test_file.write_text('[{"amount":100,"currency":"RUB","description":"test"}]')

    data = load_transactions(test_file)
    assert len(data) == 1
    assert data[0]["amount"] == Decimal("100")

def test_load_transactions_not_found():
    with pytest.raises(FileNotFoundError):
        load_transactions("nonexistent.json")