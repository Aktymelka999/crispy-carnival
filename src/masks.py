import logging

logger = logging.getLogger("src.masks")


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

def apply_mask(text: str, mask: str) -> str | None:
    if not text or len(text) < 4:
        # Ошибка: уровень ERROR
        logger.error("Не удалось применить маску: текст слишком короткий или пустой. Текст: %r, маска: %r", text, mask)
        return None

    try:
        result = mask + text[-4:]
        # Успешный случай: уровень INFO
        logger.info("Маска успешно применена: %r -> %r", text, result)
        return result
    except Exception as e:
        # Любая непредвиденная ошибка
        logger.exception("Критическая ошибка при маскировании: %s", e)
        return None