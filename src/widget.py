def mask_account_card(input_string):
    """
    Маскирует номер карты или счёта в строке.

    Для карт: оставляет первые 6 и последние 4 цифры, остальные заменяет на *.
    Для счетов: показывает только последние 4 цифры с ** впереди.

    Args:
        input_string (str): строка, содержащая тип и номер (например, "Visa 1234..." или "Счёт 123...").

    Returns:
        str: строка с замаскированным номером.
    """
    if not isinstance(input_string, str):
        return ""

    parts = input_string.split()
    if len(parts) < 2:
        return input_string

    # Ищем номер — последовательность цифр
    number = None
    for part in parts:
        if part.isdigit():
            number = part
            break

    if number is None:
        return input_string  # если номера нет, возвращаем исходную строку

    # Определяем тип: если длина >= 16 — карта, иначе счёт
    if len(number) >= 16:
        # Маскируем номер карты: первые 6 цифр и последние 4 видны
        masked_number = f"{number[:6]}**{number[-4:]}"
        # Разбиваем на блоки по 4 цифры для читаемости
        masked_number = (
            masked_number[:4] + " " +
            masked_number[4:8] + " **** " +
            masked_number[-4:]
        )
    else:
        # Для счёта показываем только последние 4 цифры
        masked_number = f"**{number[-4:]}"

    return input_string.replace(number, masked_number)



def get_date(date_string):
    """
    Извлекает дату в формате ДД.ММ.ГГГГ из строки.

    Поддерживает форматы:
    * ISO: "2023-01-15T10:30:00" → "15.01.2023"
    * Просто дата: "2023-01-15" → "15.01.2023"

    Args:
        date_string (str): исходная строка с датой.

    Returns:
        str: дата в формате ДД.ММ.ГГГГ или пустая строка при ошибке.
    """
    if not isinstance(date_string, str):
        return ""

    # Убираем время, если есть (разделитель T или пробел)
    date_part = date_string.split("T")[0] if "T" in date_string else date_string
    date_part = date_part.split()[0] if " " in date_part else date_part

    # Ожидаем формат ГГГГ-ММ-ДД
    try:
        year, month, day = map(int, date_part.split("-"))
        return f"{day:02d}.{month:02d}.{year}"
    except (ValueError, IndexError):
        return ""  # при ошибке парсинга возвращаем пустую строк