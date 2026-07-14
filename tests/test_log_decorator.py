import pytest

from src.log_decorator import log


class TestLogDecorator:
    def test_successful_execution_with_positional_args(self, capsys):
        """Тест успешного выполнения функции с позиционными аргументами (вывод в консоль)."""

        @log()
        def add(a, b):
            return a + b

        result = add(2, 3)

        assert result == 5

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 1
        assert output_lines[0] == "add ok"

    def test_successful_execution_with_kwargs(self, capsys):
        """Тест успешного выполнения функции с именованными аргументами."""

        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        assert result == "Hi, Alice!"

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 1
        assert output_lines[0] == "greet ok"

    def test_function_returning_none(self, capsys):
        """Тест функции, возвращающей None."""

        @log()
        def do_nothing():
            pass

        result = do_nothing()

        assert result is None

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 1
        assert output_lines[0] == "do_nothing ok"

    def test_multiple_calls(self, capsys):
        """Тест многократного вызова функции."""

        @log()
        def square(x):
            return x**2

        results = [square(i) for i in range(3)]

        assert results == [0, 1, 4]

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 3
        for i, line in enumerate(output_lines):
            assert line == "square ok"

    def test_exception_handling(self, capsys):
        """Тест обработки исключения: исключение возникает внутри функции."""

        @log()
        def divide(a, b):
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b

        with pytest.raises(ZeroDivisionError, match="Division by zero"):
            divide(10, 0)

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 1
        expected_error = "divide error: ZeroDivisionError. Inputs: (10, 0), {}"
        assert output_lines[0] == expected_error

    def test_no_args_function(self, capsys):
        """Тест функции без аргументов."""

        @log()
        def say_hello():
            return "Hello!"

        result = say_hello()

        assert result == "Hello!"

        captured = capsys.readouterr()
        output_lines = [line.strip() for line in captured.out.split("\n") if line.strip()]
        assert len(output_lines) == 1
        assert output_lines[0] == "say_hello ok"

    def test_logging_to_file(self, tmp_path):
        """Тест логирования в файл (при указании параметра filename)."""
        log_file = tmp_path / "test.log"

        @log(filename=str(log_file))
        def func_with_file_logging(x):
            return x * 2

        result = func_with_file_logging(5)

        assert result == 10
        assert log_file.exists()

        # Проверяем содержимое файла
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
        assert len(lines) == 1
        assert lines[0] == "func_with_file_logging ok"

    def test_exception_in_file_logging(self, tmp_path):
        """Тест обработки исключений при логировании в файл."""
        log_file = tmp_path / "error.log"

        @log(filename=str(log_file))
        def problematic_func():
            raise RuntimeError("Something went wrong")

        with pytest.raises(RuntimeError, match="Something went wrong"):
            problematic_func()

        assert log_file.exists()

        # Проверяем содержимое файла
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
        assert len(lines) == 1
        expected_error = "problematic_func error: RuntimeError. Inputs: (), {}"
        assert lines[0] == expected_error
