import argparse
from pathlib import Path

from src.loaders import load_transactions_from_file
from src.processing import filter_by_state, sort_by_date


def main() -> None:
    parser = argparse.ArgumentParser(description="Виджет банковских операций")
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Путь к файлу с транзакциями (CSV/XLSX)",
    )
    args = parser.parse_args()

    file_path = Path(args.data)
    transactions = load_transactions_from_file(str(file_path))

    filtered = filter_by_state(transactions, "COMPLETED")
    sorted_tx = sort_by_date(filtered)

    print(f"Загружено: {len(transactions)} транзакций")
    print(f"После фильтрации: {len(filtered)}")
    print(f"Отсортировано: {len(sorted_tx)}")


if __name__ == "__main__":
    main()
