import argparse
from pathlib import Path
from typing import List, Dict, Any

from src.loaders import load_csv_transactions, load_xlsx_transactions
from src.processing import filter_by_state, sort_by_date


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Обёртка, которая выбирает нужную функцию загрузки по расширению файла.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_csv_transactions(file_path)
    elif suffix in (".xlsx", ".xls"):
        return load_xlsx_transactions(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Виджет банковских операций")
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Путь к файлу с транзакциями (CSV/XLSX)",
    )
    args = parser.parse_args()

    file_path = str(Path(args.data))
    transactions = load_transactions(file_path)

    filtered = filter_by_state(transactions, "COMPLETED")
    sorted_tx = sort_by_date(filtered)

    print(f"Загружено: {len(transactions)} транзакций")
    print(f"После фильтрации: {len(filtered)}")
    print(f"Отсортировано: {len(sorted_tx)}")


if __name__ == "__main__":
    main()
