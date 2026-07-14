import functools
import logging
import sys
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def log(filename: Optional[str] = None):
    """
    Декоратор для логирования начала и конца выполнения функции, а также её результатов или ошибок.

    Args:
        filename: путь к файлу для записи логов. Если None, логи выводятся в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Создаём логгер
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            logger.propagate = False  # Отключаем передачу вверх по иерархии

            # Очищаем существующие обработчики
            logger.handlers.clear()

            # Настраиваем обработчик в зависимости от параметра filename
            if filename is not None:
                # Логирование в файл
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                # Логирование в консоль (stdout)
                handler = logging.StreamHandler(sys.stdout)

            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                # Логируем начало выполнения (по условию не требуется, но полезно для отладки)
                # logger.info(f"{func.__name__} started")

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                # Логируем ошибку с указанием типа и входных параметров
                error_msg = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                logger.error(error_msg)
                # Перебрасываем исключение дальше
                raise e
            finally:
                # Обязательно удаляем обработчик и закрываем его
                logger.removeHandler(handler)
                handler.close()

        return wrapper

    return decorator


T = TypeVar("T", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def log_call(func: T) -> T:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug("Вызов %s с args=%r, kwargs=%r", func.__name__, args, kwargs)
        try:
            result = func(*args, **kwargs)
            logger.debug("%s вернул результат: %r", func.__name__, result)
            return result
        except Exception as e:
            logger.exception("%s завершился с ошибкой: %s", func.__name__, e)
            raise

    return wrapper
