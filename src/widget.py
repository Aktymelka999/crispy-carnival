from datetime import datetime

def _mask_card_number(card_number: str) -> str:
    """Маскирует номер карты по шаблону: XXXX XX** **** XXXX"""
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать ровно 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

def _mask_account_number(account_number: str) -> str:
    """Маскирует номер счёта по шаблону: **XXXX (только последние 4 цифры)"""
    if len(account_number) != 20 or not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать ровно 20 цифр")
    return f"**{account_number[-4:]}"

def mask_account_card(input_string: str) -> str:
    """Обрабатывает строку с типом и номером карты/счёта и возвращает замаскированный номер."""
    parts = input_string.strip().split()
    number = parts[-1]

    is_account = any(word.lower() in input_string.lower() for word in ['счёт', 'account'])

    try:
        if is_account:
            masked_number = _mask_account_number(number)
            return f"Счёт {masked_number}"
        else:
            masked_number = _mask_card_number(number)
            card_name = ' '.join(parts[:-1])
            return f"{card_name} {masked_number}"
    except ValueError as e:
        return f"Ошибка: {e}"

def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): строка с датой в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: строка с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024")

    Raises:
        ValueError: если строка не соответствует ожидаемому формату
    """
    try:
        # Парсим дату из строки формата ISO 8601
        dt = datetime.fromisoformat(date_string)
        # Форматируем в нужный вид
        formatted_date = dt.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {date_string}. Ожидаемый формат: YYYY-MM-DDTHH:MM:SS.ssssss") from e