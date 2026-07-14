import logging
import pytest
from src.log_decorator import log_execution


class TestLogDecorator:
    def test_successful_execution_with_positional_args(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)

        @log_execution()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(2, 3)
        assert result == 5

        assert len(caplog.records) == 1
        assert caplog.records[0].message == "add ok"

    def test_successful_execution_with_kwargs(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)

        @log_execution()
        def greet(name: str, greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")
        assert result == "Hi, Alice!"

        assert len(caplog.records) == 1
        assert caplog.records[0].message == "greet ok"

    def test_function_returning_none(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)

        @log_execution()
        def do_nothing() -> None:
            pass

        result = do_nothing()
        assert result is None

        assert len(caplog.records) == 1
        assert caplog.records[0].message == "do_nothing ok"

    def test_multiple_calls(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)

        @log_execution()
        def square(x: int) -> int:
            return x**2

        results = [square(i) for i in range(3)]
        assert results == [0, 1, 4]

        # 3 вызова → 3 записи в логе
        assert len(caplog.records) == 3
        for record in caplog.records:
            assert record.message == "square ok"

    def test_exception_handling(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.ERROR)

        @log_execution()
        def divide(a: int, b: int) -> float:
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            divide(10, 0)

        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelno == logging.ERROR
        assert "divide error: ZeroDivisionError" in record.message
        assert "(10, 0)" in record.message or "Inputs: (10, 0)" in record.message

    def test_no_args_function(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)

        @log_execution()
        def say_hello() -> str:
            return "Hello!"

        result = say_hello()
        assert result == "Hello!"

        assert len(caplog.records) == 1
        assert caplog.records[0].message == "say_hello ok"

    def test_logging_to_file(self, tmp_path, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        log_file = tmp_path / "test.log"

        @log_execution(filename=str(log_file))
        def func_with_file_logging(x: int) -> int:
            return x * 2

        result = func_with_file_logging(5)
        assert result == 10
        assert log_file.exists()

        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
        assert len(lines) == 1
        assert lines[0] == "func_with_file_logging ok"

    def test_exception_in_file_logging(self, tmp_path, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.ERROR)
        log_file = tmp_path / "error.log"

        @log_execution(filename=str(log_file))
        def problematic_func() -> None:
            raise RuntimeError("Something went wrong")

        with pytest.raises(RuntimeError, match="Something went wrong"):
            problematic_func()

        assert log_file.exists()
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
        assert len(lines) == 1
        line = lines[0]
        assert "problematic_func error: RuntimeError" in line
