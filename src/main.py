from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from loaders import (
    load_csv_transactions,
    load_json_transactions,
    load_xlsx_transactions,
)
from processing import filter_by_state, process_bank_search, sort_by_date
from utils import get_amount_decimal, get_currency_code

AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def get_file_path_from_menu() -> Optional[str]:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice in ("1", "2", "3"):
            file_type = {"1": "JSON", "2": "CSV", "3": "XLSX"}[choice]
            print(f"Программа: Для обработки выбран {file_type}-файл.")
            path = input(f"Программа: Укажите путь к {file_type}-файлу: ").strip()
            return path
        else:
            print("Программа: Неверный выбор пункта меню. Пожалуйста, выберите 1, 2 или 3.")


def get_status_filter() -> str:
    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}")
        user_input = input("Пользователь: ").strip()
        normalized = user_input.upper()
        if normalized in AVAILABLE_STATUSES:
            print(f'Программа: Операции отфильтрованы по статусу "{normalized}"')
            return normalized
        else:
            print(f'Программа: Статус операции "{user_input}" недоступен. Попробуйте снова.')


def ask_yes_no(question: str) -> bool:
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        elif answer in ("нет", "н", "no", "n"):
            return False
        else:
            print("Программа: Пожалуйста, ответьте Да или Нет.")


def ask_sort_order() -> str:
    while True:
        order = input("Программа: Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if "возр" in order or "asc" in order:
            return "asc"
        elif "убыв" in order or "desc" in order:
            return "desc"
        else:
            print("Программа: Пожалуйста, укажите «по возрастанию» или «по убыванию».")


def format_date(date_raw: Any) -> str:
    if not isinstance(date_raw, str):
        return str(date_raw)
    if "T" in date_raw:
        date_raw = date_raw.split("T")[0]
    parts = date_raw.split("-")
    if len(parts) == 3:
        try:
            year, month, day = parts
            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                return f"{day}.{month}.{year}"
        except Exception:
            pass
    return str(date_raw)


def format_transaction(tx: Dict[str, Any]) -> str:
    date_raw = tx.get("date", "")
    date_fmt = format_date(date_raw)

    desc = tx.get("description", "Без описания")
    currency_code = get_currency_code(tx) or "?"
    amount = get_amount_decimal(tx)

    lines = [f"{date_fmt} {desc}"]

    from_acc = tx.get("from", "")
    to_acc = tx.get("to", "")
    if from_acc or to_acc:
        lines.append(f"{from_acc} → {to_acc}")

    if amount is not None:
        amount_str = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
    else:
        amount_str = "0,00"

    lines.append(f"Сумма: {amount_str} {currency_code}")
    return "\n".join(lines)


def apply_sorting(transactions: List[Dict[str, Any]], ask_sort: bool) -> List[Dict[str, Any]]:
    if not ask_sort:
        return transactions

    order = ask_sort_order()
    try:
        sorted_tx = sort_by_date(transactions)
    except Exception as e:
        print(f"Программа: Ошибка при сортировке по дате: {e}")
        return transactions

    if order == "desc":
        sorted_tx.reverse()
    return sorted_tx  # type: ignore[no-any-return]


def apply_currency_filter(transactions: List[Dict[str, Any]], ask_currency: bool) -> List[Dict[str, Any]]:
    if not ask_currency:
        return transactions

    result: List[Dict[str, Any]] = []
    for tx in transactions:
        if get_currency_code(tx) == "RUB":
            result.append(tx)
    return result


def apply_search_filter(transactions: List[Dict[str, Any]], ask_search: bool) -> List[Dict[str, Any]]:
    if not ask_search:
        return transactions

    search_term = input("Пользователь: Введите слово для поиска в описании: ").strip()
    if not search_term:
        return transactions

    try:
        raw_result = process_bank_search(transactions, search_term)
        return cast(List[Dict[str, Any]], raw_result)
    except Exception as e:
        print(f"Программа: Ошибка при поиске: {e}")
        return transactions


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден по пути: {path.resolve()}")

    suffix = path.suffix.lower()
    print(f"Программа: Выбран файл: {path.name} (формат: {suffix})")

    raw_data: Any = []
    if suffix == ".json":
        raw_data = load_json_transactions(file_path)
    elif suffix == ".csv":
        raw_data = load_csv_transactions(file_path)
    elif suffix in (".xlsx", ".xls"):
        raw_data = load_xlsx_transactions(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {suffix}")

    return cast(List[Dict[str, Any]], raw_data)


def run_pipeline(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    status_filter = get_status_filter()
    filtered = filter_by_state(transactions, status_filter)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции с указанным статусом.")
        return []

    ask_sort = ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ")
    sorted_tx = apply_sorting(filtered, ask_sort)

    ask_currency = ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ")
    currency_tx = apply_currency_filter(sorted_tx, ask_currency)

    ask_search = ask_yes_no(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\nПользователь: "
    )
    final_tx = apply_search_filter(currency_tx, ask_search)

    return final_tx


def main() -> None:
    file_path = get_file_path_from_menu()
    if not file_path or not file_path.strip():
        print("Программа: Путь к файлу не был указан.")
        return

    try:
        transactions = load_transactions(file_path)
    except FileNotFoundError as e:
        print(e)
        return
    except ValueError as e:
        print(e)
        return
    except Exception as e:
        print(f"Программа: Ошибка при чтении файла: {e}")
        return

    if not transactions:
        print("Программа: Файл пуст или не содержит корректных данных.")
        return

    final_tx = run_pipeline(transactions)

    if not final_tx:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(f"\nПрограмма: Всего банковских операций в выборке: {len(final_tx)}\n")
    for tx in final_tx:
        print(format_transaction(tx))
        print("-" * 40)


if __name__ == "__main__":
    main()
