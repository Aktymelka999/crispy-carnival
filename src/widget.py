
def mask_account_card(input_string: str) -> str:
    if not isinstance(input_string, str) or not input_string.strip():
        return ""  # Возвращаем пустую строку для пустого/некорректного ввода
    parts = input_string.split()
    if len(parts) < 2:
        return input_string

    # Извлекаем номер — последовательность цифр
    number = None
    for part in parts:
        if part.isdigit():
            number = part
            break

    if number is None:
        return input_string

    # Определяем тип: если в начале строки есть «Счёт», то это счёт
    is_account = any(word.lower() in input_string.lower() for word in ['счёт', 'account'])
    if is_account:
        # Для счёта показываем только последние 4 цифры
        masked = f"**{number[-4:]}"
    else:
        # Для карты: первые 6 и последние 4 цифры видны, остальное маскируем
        if len(number) >= 16:
            masked_part = f"{number[:6]}**{number[-4:]}"
            # Форматируем с пробелами: XXXX XX** **** XXXX
            masked = (
                masked_part[:4] + " " +
                masked_part[4:8] + " **** " +
                number[-4:]
            )
        else:
            # Если номер короткий, но не счёт — возвращаем как есть
            masked = number

    return input_string.replace(number, masked)

from datetime import datetime

def get_date(date_string: str) -> str:
    """
    Преобразует строку даты в формате 'YYYY-MM-DDTHH:MM:SS' в 'DD.MM.YYYY'.
    """
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты")