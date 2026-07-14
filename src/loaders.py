from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


def _normalize_date(value: Optional[Any]) -> str:
    """
    Приводит дату к формату YYYY-MM-DD или возвращает пустую строку.

    Args:
        value: Исходное значение даты (может быть строкой, pandas.Timestamp, None и т.п.)

    Returns:
        Строка в формате YYYY-MM-DD либо пустая строка.
    """
    if value is None:
        return ""

    value_str = str(value).strip()
    if not value_str:
        return ""

    # Быстрая проверка на уже корректный формат YYYY-MM-DD
    if len(value_str) == 10 and value_str[4] == "-" and value_str[7] == "-":
        # Дополнительно можно проверить, что остальные символы — цифры, но пока оставим так
        return value_str

    try:
        dt = pd.to_datetime(value_str, errors="raise")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        # Если не получилось распарсить — возвращаем пустую строку, чтобы не ломать логику
        return ""


def load_transactions_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из CSV или XLSX и возвращает список словарей.

    Поддерживаемые форматы: .csv, .xlsx

    Args:
        file_path: Путь к файлу с транзакциями.

    Returns:
        Список словарей с нормализованными транзакциями.

    Raises:
        FileNotFoundError: Если файл не найден.
        ValueError: Если формат файла не поддерживается.
        RuntimeError: Если не удалось прочитать CSV (например, неподходящая кодировка).
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    suffix = path.suffix.lower()

    df: Optional[pd.DataFrame] = None

    if suffix == ".csv":
        for enc in ["utf-8", "cp1251"]:
            try:
                df = pd.read_csv(path, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise RuntimeError("Не удалось прочитать CSV ни в UTF‑8, ни в CP1251")

    elif suffix == ".xlsx":
        df = pd.read_excel(path, engine="openpyxl")
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")

    records = df.to_dict(orient="records")
    normalized: List[Dict[str, Any]] = []

    for row in records:
        if not row.get("id"):
            continue

        normalized_row: Dict[str, Any] = {
            "id": str(row["id"]),
            "amount": float(row.get("amount", 0)),
            "currency": str(row.get("currency", "RUB")),
            "type": str(row.get("type", "UNKNOWN")),
            "state": str(row.get("state", "PENDING")),
            "date": _normalize_date(row.get("date")),
            "description": str(row.get("description", "")),
        }
        normalized.append(normalized_row)

    return normalized
