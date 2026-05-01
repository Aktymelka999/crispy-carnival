import pytest
from src.widget import mask_account_card, get_date  # импорт get_date добавлен

class TestWidgetFunctions:
    @pytest.mark.parametrize("input_str,expected", [
        ("Счёт 12345678901234567890", "Счёт **7890"),
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
        ("", ""),  # пустая строка → пустая строка
        ("Без номера", "Без номера"),
    ])
    def test_mask_account_card_valid(self, input_str, expected):
        assert mask_account_card(input_str) == expected

    def test_mask_account_card_empty_input(self):
        result = mask_account_card("")
        assert result == ""  # исправлено: ожидаем пустую строку


    @pytest.mark.parametrize("date_input,expected", [
        ("2023-01-01T12:00:00", "01.01.2023"),
        ("2024-12-31T23:59:59", "31.12.2024")
    ])
    def test_get_date_valid(self, date_input, expected):
        assert get_date(date_input) == expected  # get_date теперь доступен


    def test_get_date_invalid_format(self):
        with pytest.raises(ValueError):
            get_date("некорректная_дата")  # get_date теперь доступен