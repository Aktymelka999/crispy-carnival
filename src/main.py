from src.widget import get_date, mask_account_card
from utils import load_transactions
from widget import BankWidget  # класс  в widget.py

import logging

import logging
import os
from pathlib import Path


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
        "Счет 73654108430135874305",
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


root_dir = Path(__file__).resolve().parents[1]
logs_dir = root_dir / "logs"
logs_dir.mkdir(exist_ok=True)

# Формат: время | модуль | уровень | сообщение
log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(log_format, datefmt=date_format)


def setup_module_logger(module_name: str, log_filename: str) -> logging.Logger:
    """Создаёт отдельный логгер с file_handler именно для этого модуля."""
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Уровень не меньше DEBUG
    
    # Очищаем старые хендлеры
    if logger.handlers:
        logger.handlers.clear()

    
    file_path = logs_dir / log_filename
    file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger



logger_utils = setup_module_logger("src.utils", "utils.log")
logger_masks = setup_module_logger("src.masks", "masks.log")