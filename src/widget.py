from datetime import datetime

from src.masks import mask_account_number, mask_card_number


def mask_account_card(input_string: str) -> str:
    """
    Обрабатывает строку с типом и номером карты/счёта и возвращает замаскированный номер.

    Args:
        input_string (str): строка с типом и номером

    Returns:
        str: строка с замаскированным номером
    """
    parts = input_string.strip().split()
    number = parts[-1]  # последняя часть — номер

    is_account = any(word.lower() in input_string.lower() for word in ['счёт', 'account'])

    try:
        if is_account:
            masked_number = mask_account_number(number)
            return f"Счёт {masked_number}"
        else:
            # Считаем, что всё остальное — карта
            masked_number = mask_card_number(number)
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
        dt = datetime.fromisoformat(date_string)
        formatted_date = dt.strftime("%d.%m.%Y")
        return formatted_date
    except ValueError as e:
        raise ValueError(
            f"Некорректный формат даты: {date_string}. "
            "Ожидаемый формат: YYYY-MM-DDTHH:MM:SS.ssssss"
        ) from e
