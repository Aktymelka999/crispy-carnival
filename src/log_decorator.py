import functools
import logging
from logging import FileHandler, StreamHandler
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])


def log_execution(logger_name: str = "app", filename: str | None = None) -> Callable[[T], T]:
    """
    Декоратор, который логирует вызов функции.

    Args:
        logger_name: Имя логгера.
        filename: Если указано, добавит FileHandler в этот файл.

    Returns:
        Декоратор для функции.
    """
    logger = logging.getLogger(logger_name)

    if not any(isinstance(h, FileHandler) and h.baseFilename == filename for h in logger.handlers):
        if filename is not None:
            file_handler = FileHandler(filename, encoding="utf-8")
            formatter = logging.Formatter("%(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    if not any(isinstance(h, StreamHandler) for h in logger.handlers):
        stream_handler = StreamHandler()
        formatter = logging.Formatter("%(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)

    def decorator(func: T) -> T:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            args_repr = ", ".join(repr(a) for a in args)
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            inputs = f"({args_repr}"
            if kwargs_repr:
                inputs += f", {kwargs_repr}"
            inputs += ")"

            try:
                result = func(*args, **kwargs)
                logger.info("%s ok", func.__name__)
                return result
            except Exception as e:
                logger.error("%s error: %s. Inputs: %s, {}", func.__name__, type(e).__name__, inputs)
                raise

        return cast(T, wrapper)

    return decorator
