from typing import List, Dict, Any, Optional
from pathlib import Path
from src.loaders import load_csv_transactions, load_xlsx_transactions, load_json_transactions
from src.processing import filter_by_state, sort_by_date, process_bank_search, filter_by_currency
from src.utils import get_currency_code, get_amount_decimal

AVAILABLE_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def get_file_path_from_menu() -> Optional[str]:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            path = input("Программа: Укажите путь к JSON-файлу: ").strip()
            return path
        elif choice == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            path = input("Программа: Укажите путь к CSV-файлу: ").strip()
            return path
        elif choice == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            path = input("Программа: Укажите путь к XLSX-файлу: ").strip()
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
            print(f'Программа: Статус операции "{user_input}" недоступен.')


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


def format_transaction(tx: Dict[str, Any]) -> str:
    date_raw = tx.get("date", "")
    if isinstance(date_raw, str) and len(date_raw) > 10 and date_raw[10] == "T":
        date_raw = date_raw[:10]

    if len(date_raw) == 10 and date_raw[4] == "-" and date_raw[7] == "-":
        date_fmt = f"{date_raw[8:10]}.{date_raw[5:7]}.{date_raw[0:4]}"
    else:
        date_fmt = date_raw

    desc = tx.get("description", "Без описания")
    currency_code = get_currency_code(tx) or "?"
    amount = get_amount_decimal(tx)

    lines = [f"{date_fmt} {desc}"]

    from_acc = tx.get("from", "")
    to_acc = tx.get("to", "")
    if from_acc or to_acc:
        lines.append(f"{from_acc} → {to_acc}")

    amount_str = f"{amount:,.2f}".replace(",", " ")
    lines.append(f"Сумма: {amount_str} {currency_code}")

    return "\n".join(lines)


def apply_sorting(transactions: List[Dict[str, Any]], ask_sort: bool) -> List[Dict[str, Any]]:
    if not ask_sort:
        return transactions
    order = ask_sort_order()
    sorted_tx = sort_by_date(transactions)
    if order == "desc":
        sorted_tx.reverse()
    return sorted_tx


def apply_currency_filter(transactions: List[Dict[str, Any]], ask_currency: bool) -> List[Dict[str, Any]]:
    if not ask_currency:
        return transactions
    return filter_by_currency(transactions, "RUB")


def apply_search_filter(transactions: List[Dict[str, Any]], ask_search: bool) -> List[Dict[str, Any]]:
    if not ask_search:
        return transactions
    search_term = input("Пользователь: ").strip()
    return process_bank_search(transactions, search_term)


def main() -> None:
    file_path = get_file_path_from_menu()
    if file_path is None or not file_path.strip():
        print("Программа: Путь к файлу не был указан.")
        return

    path = Path(file_path)
    suffix = path.suffix.lower()

    try:
        if suffix == ".json":
            transactions = load_json_transactions(file_path)
        elif suffix == ".csv":
            transactions = load_csv_transactions(file_path)
        elif suffix in (".xlsx", ".xls"):
            transactions = load_xlsx_transactions(file_path)
        else:
            print(f"Программа: Неподдерживаемый формат файла: {suffix}")
            return
    except FileNotFoundError:
        print(f"Программа: Файл не найден: {file_path}")
        return
    except Exception as e:
        print(f"Программа: Ошибка при чтении файла: {e}")
        return

    status_filter = get_status_filter()
    filtered = filter_by_state(transactions, status_filter)

    ask_sort = ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\nПользователь: ")
    sorted_tx = apply_sorting(filtered, ask_sort)

    ask_currency = ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\nПользователь: ")
    currency_tx = apply_currency_filter(sorted_tx, ask_currency)

    ask_search = ask_yes_no(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\nПользователь: "
    )
    final_tx = apply_search_filter(currency_tx, ask_search)

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    if not final_tx:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nПрограмма: Всего банковских операций в выборке: {len(final_tx)}\n")
    for tx in final_tx:
        print(format_transaction(tx))
        print()


if __name__ == "__main__":
    main()
