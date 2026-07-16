import csv
import json
from typing import List, Dict, Any

try:
    import pandas as pd
except ImportError:
    pd = None


def load_csv_transactions(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{str(k): v for k, v in row.items()} for row in reader]


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
