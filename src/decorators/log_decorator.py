import functools
import logging
from typing import Optional

def log(filename: Optional[str] = None):
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также её результатов или возникших ошибок.

    Параметры:
        filename (str, optional): имя файла для записи логов.
            Если None — логи выводятся в консоль.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Настройка логгера
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            # Очищаем обработчики, чтобы не дублировать логи
            logger.handlers.clear()

            if filename:
                # Логирование в файл
                handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
            else:
                # Логирование в консоль
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                # Логируем начало выполнения
                logger.info(f"{func.__name__} started")

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешный результат
                logger.info(f"{func.__name__} ok")
                return result

            except Exception as e:
                # Логируем ошибку с типом ошибки и входными параметрами
                error_msg = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                logger.error(error_msg)
                raise e

            finally:
                # Удаляем обработчик после использования
                logger.removeHandler(handler)

        return wrapper
    return decorator

import functools
import logging
from typing import Optional

def log(filename: Optional[str] = None):
    """
    Декоратор для логирования начала и конца выполнения функции,
    а также её результатов или возникших ошибок.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            logger.handlers.clear()

            if filename:
                handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                logger.info(f"{func.__name__} started")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                error_msg = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                logger.error(error_msg)
                raise e
            finally:
                logger.removeHandler(handler)

        return wrapper
    return decorator