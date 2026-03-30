#!/usr/bin/env python3
"""
Точка входа в консольное приложение для обработки данных.
"""

import sys
import logging
import argparse

from config import load_config
from services.database import Database
from core.processor import DataProcessor

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description='Обработка данных')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    parser.add_argument('--config', type=str, default='config.yaml', help='Файл конфигурации')
    return parser.parse_args()

def main():
    args = parse_arguments()
    config = load_config(args.config)
    db = Database(config['database_url'])
    processor = DataProcessor(db)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Запуск обработки данных...")
    processor.process()
    logger.info("Обработка завершена.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")
        sys.exit(1)