def mask_card_number(card_number: str) -> str:
    """Маскирует номер карты по шаблону: XXXX XX** **** XXXX"""
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать ровно 16 цифр")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def mask_account_number(account_number: str) -> str:
    """Маскирует номер счёта по шаблону: **XXXX (только последние 4 цифры)"""
    if len(account_number) != 20 or not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать ровно 20 цифр")
    return f"**{account_number[-4:]}"
