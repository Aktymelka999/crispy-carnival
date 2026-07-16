import pytest

try:
    import pandas as pd
except ImportError:
    pd = None

from src.loaders import load_csv_transactions, load_xlsx_transactions


@pytest.fixture
def sample_csv_path(tmp_path):
    """Создаёт временный CSV-файл с тестовыми данными."""
    csv_file = tmp_path / "transactions.csv"
    # Пробел после # обязателен для Flake8
    csv_content = "id,currency,amount\n1,RUB,100\n2,USD,200"
    csv_file.write_text(csv_content, encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def sample_xlsx_path(tmp_path):
    """Создаёт временный XLSX-файл (требуется pandas)."""
    if pd is None:
        pytest.skip("pandas not installed, skipping XLSX test")

    xlsx_file = tmp_path / "transactions.xlsx"
    df = pd.DataFrame(
        [
            {"id": 1, "currency": "RUB", "amount": 100},
            {"id": 2, "currency": "USD", "amount": 200},
        ]
    )
    df.to_excel(str(xlsx_file), index=False)
    return str(xlsx_file)


def test_load_csv_returns_list_of_dicts(sample_csv_path):
    data = load_csv_transactions(sample_csv_path)
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(isinstance(row, dict) for row in data)


def test_load_xlsx_returns_list_of_dicts(sample_xlsx_path):
    data = load_xlsx_transactions(sample_xlsx_path)
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(isinstance(row, dict) for row in data)
