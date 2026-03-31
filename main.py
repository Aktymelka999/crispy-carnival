from src.widget import get_date, mask_account_card


def main():
    # Тестовые случаи для маскировки карт и счетов
    card_test_cases = [
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383033474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305"
    ]

    date_test_case = "2024-03-11T02:26:18.671407"

    print("=== ТЕСТИРОВАНИЕ МАСКИРОВКИ КАРТ И СЧЕТОВ ===")
    for case in card_test_cases:
        result = mask_account_card(case)
        print(f"Вход: {case}")
        print(f"Выход: {result}")
        print("-" * 60)

    print("\n=== ТЕСТИРОВАНИЕ ФУНКЦИИ get_date ===")
    print(f"Вход: {date_test_case}")
    result_date = get_date(date_test_case)
    print(f"Выход: {result_date}")


if __name__ == "__main__":
    main()
