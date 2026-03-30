def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты, оставляя видимыми первые 6 цифр и последние 4 цифры.
    Формат вывода: XXXX XX** **** XXXX (блоки по 4 символа, разделённые пробелами).

    Args:
        card_number (str): Номер банковской карты (16 цифр, может содержать пробелы/дефисы).

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX.

    Example:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, card_number))
    
    # Проверяем длину — должна быть 16 цифр
    if len(digits) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    
    # Формируем блоки по заданию:
    # - первые 4 цифры (XXXX)
    # - следующие 2 цифры (XX)
    # - 4 скрытые цифры (** **)
    # - последние 4 цифры (XXXX)
    block1 = digits[0:4]    # XXXX
    block2 = digits[4:6]    # XX
    block3 = '** **'        # **** (в формате ** **)
    block4 = digits[-4:]    # XXXX
    
    # Объединяем блоки с пробелами
    masked_number = ' '.join([block1, block2, block3, block4])
    
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта, оставляя видимыми только последние 4 цифры.
    Формат вывода: **XXXX (без пробелов, только две звёздочки + последние 4 цифры).

    Args:
        account_number (str): Номер банковского счёта (20 цифр, может содержать пробелы/дефисы).

    Returns:
        str: Замаскированный номер счёта в формате **XXXX.

    Example:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, account_number))
    
    # Проверяем длину — должна быть 20 цифр
    if len(digits) != 20:
        raise ValueError("Номер счёта должен содержать 20 цифр")
    
    # Формируем маску: две звёздочки + последние 4 цифры
    masked_account = '**' + digits[-4:]
    
    return masked_account