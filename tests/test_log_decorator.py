import pytest
import logging
from decorators.log_decorator import log


class TestLogDecorator:
    def test_successful_execution_with_positional_args(self, caplog):
        """Тест успешного выполнения функции с позиционными аргументами."""
        @log()
        def add(a, b):
            return a + b

        with caplog.at_level(logging.INFO):
            result = add(2, 3)

        assert result == 5
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "add started"
        assert caplog.records[1].message == "add ok"

    def test_successful_execution_with_kwargs(self, caplog):
        """Тест успешного выполнения функции с именованными аргументами."""
        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        with caplog.at_level(logging.INFO):
            result = greet("Alice", greeting="Hi")

        assert result == "Hi, Alice!"
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "greet started"
        assert caplog.records[1].message == "greet ok"

    def test_function_returning_none(self, caplog):
        """Тест функции, возвращающей None."""
        @log()
        def do_nothing():
            pass

        with caplog.at_level(logging.INFO):
            result = do_nothing()

        assert result is None
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "do_nothing started"
        assert caplog.records[1].message == "do_nothing ok"

    def test_multiple_calls(self, caplog):
        """Тест многократного вызова функции."""
        @log()
        def square(x):
            return x ** 2

        with caplog.at_level(logging.INFO):
            results = [square(i) for i in range(3)]

        assert results == [0, 1, 4]
        assert len(caplog.records) == 6
        for i in range(3):
            assert caplog.records[i * 2].message == "square started"
            assert caplog.records[i * 2 + 1].message == "square ok"

    def test_exception_handling(self, caplog):
        """Тест обработки исключения: исключение возникает внутри функции."""
        @log()
        def divide(a, b):
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

        with caplog.at_level(logging.INFO):
            with pytest.raises(ZeroDivisionError, match="Division by zero"):
                divide(10, 0)

        assert len(caplog.records) == 2
        assert caplog.records[0].message == "divide started"
        expected_error = "divide error: ZeroDivisionError. Inputs: (10, 0), {}"
        assert caplog.records[1].message == expected_error

    def test_exception_before_execution(self, caplog):
        """Тест: исключение возникает до вызова декорированной функции (в декораторе)."""
        # Для демонстрации создадим декоратор, который может выбросить исключение до вызова функции.
        # В нашем случае это не применимо напрямую, поэтому проверим, что декоратор корректно обрабатывает
        # исключения, возникающие в декорируемой функции.
        @log()
        def problematic_func():
            raise RuntimeError("Something went wrong")

        with caplog.at_level(logging.INFO):
            with pytest.raises(RuntimeError, match="Something went wrong"):
                problematic_func()

        assert len(caplog.records) == 2
        assert caplog.records[0].message == "problematic_func started"
        expected_error = "problematic_func error: RuntimeError. Inputs: (), {}"
        assert caplog.records[1].message == expected_error

    def test_logging_to_file(self, tmp_path, caplog):
        """Тест логирования в файл (при указании параметра filename)."""
        log_file = tmp_path / "test.log"

        @log(filename=str(log_file))
        def func_with_file_logging(x):
            return x * 2

        with caplog.at_level(logging.INFO):
            result = func_with_file_logging(5)

        assert result == 10
        assert log_file.exists()

        # Проверяем содержимое файла
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split('\n')
        assert len(lines) == 2
        assert lines[0] == "func_with_file_logging started"
        assert lines[1] == "func_with_file_logging ok"

    def test_no_args_function(self, caplog):
        """Тест функции без аргументов."""
        @log()
        def say_hello():
            return "Hello!"

        with caplog.at_level(logging.INFO):
            result = say_hello()

        assert result == "Hello!"
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "say_hello started"
        assert caplog.records[1].message == "say_hello ok"