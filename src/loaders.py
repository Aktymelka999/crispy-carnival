import csv
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import pandas as pd
except ImportError:
    pd = None


def load_csv_transactions(filepath: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из CSV файла с разделителем ';'.

    Args:
        filepath: Относительный или абсолютный путь к файлу.

    Returns:
        Список словарей с данными транзакций.
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл транзакций не найден: {file_path.resolve()}")

    transactions = []

    with file_path.open("r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:

            clean_row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

            if any(clean_row.values()):
                transactions.append(clean_row)

    return transactions


def load_xlsx_transactions(filepath: str) -> List[Dict[str, Any]]:
    if pd is None:
        raise ImportError("pandas required for XLSX loading")
    df = pd.read_excel(filepath)
    return df.to_dict(orient="records")


def load_json_transactions(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    raise ValueError("JSON должен содержать список транзакций")
