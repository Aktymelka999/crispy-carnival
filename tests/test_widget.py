import pytest
from widget import mask_account_card, get_date

class TestMaskAccountCard:
    @pytest.mark.parametrize("input_data,expected", [
        # Номера карт (16 цифр)
        ("1234567890123456", "1234 56** **** 3456"),
        ("4444333322221111", "4444 33** **** 1111"),
        # Номера счетов (20 цифр)
        ("12345678901234567890", "**7890"),
        # С пробелами в номере карты
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        # С дефисами в номере счёта
        ("1234-5678-9012-3456-7890", "**7890"),
        # Американ Экспресс (15 цифр)
        ("378282246310005", "3782 82** **** 005"),
    ])
    def test_correct_masking(self, input_data, expected):
        """Тест корректного распознавания и маскирования карт и счетов."""
        result = mask_account_card(input_data)
        assert result == expected

    @pytest.mark.parametrize("invalid_input,expected_error", [
        ("", "Invalid input: no data provided"),
        ("abcdefghijklmnop", "Invalid input: cannot determine type"),
        ("123", "Invalid input: too short"),
        (None, "Invalid input: None value"),
        ("2023-01-01", "Invalid input: cannot determine type"),  # Дата вместо номера
    ])
    def test_invalid_inputs(self, invalid_input, expected_error):
        """Тест обработки некорректных входных данных."""
        with pytest.raises(ValueError, match=expected_error):
            mask_account_card(invalid_input)


class TestGetDate:
    @pytest.mark.parametrize("date_string,expected", [
        # Стандартные форматы
        ("2023-12-25", "25.12.2023"),
        ("2023/12/25", "25.12.2023"),
        ("25.12.2023", "25.12.2023"),
        # С временем
        ("2023-12-25T10:30:00", "25.12.2023"),
        ("2023-12-25 10:30:00", "25.12.2023"),
        # Разные разделители
        ("2023.12.25", "25.12.2023"),
    ])
    def test_valid_date_formats(self, date_string, expected):
        """Тест преобразования даты из разных форматов."""
        result = get_date(date_string)
        assert result == expected

    @pytest.mark.parametrize("edge_case,expected", [
        # Граничные случаи дат
        ("2000-01-01", "01.01.2000"),  # Начало века
        ("2100-12-31", "31.12.2100"),  # Конец века
        ("2023-02-28", "28.02.2023"),  # Последний день февраля
        ("2024-02-29", "29.02.2024"),  # Високосный год
    ])
    def test_edge_cases_dates(self, edge_case, expected):
        """Тест граничных случаев дат."""
        result = get_date(edge_case)
        assert result == expected

    def test_no_date_in_string(self):
        """Тест когда во входной строке отсутствует дата."""
        with pytest.raises(ValueError, match="Invalid date format: no valid date found"):
            get_date("No date here")

    @pytest.mark.parametrize("invalid_date,expected_error", [
        ("", "Invalid date format: empty string"),
        ("abc", "Invalid date format: cannot parse"),
        ("2023-13-01", "Invalid date format: month out of range"),
        ("2023-00-01", "Invalid date format: month out of range"),
        ("2023-01-32", "Invalid date format: day out of range"),
        ("2023/99/99", "Invalid date format: cannot parse"),
    ])
    def test_invalid_date_formats(self, invalid_date, expected_error):
        """Тест обработки некорректных форматов дат."""
        with pytest.raises(ValueError, match=expected_error):
            get_date(invalid_date)