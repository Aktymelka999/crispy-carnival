import pytest
from src.widget import mask_account_card, get_date

class TestWidget:
    @pytest.mark.parametrize("input_str,expected", [
        ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
        ("Счёт 12345678901234567890", "Счёт **7890")
    ])
    def test_mask_account_card_valid(self, input_str, expected):
        assert mask_account_card(input_str) == expected

    def test_mask_account_card_empty_input(self):
        result = mask_account_card("")
        assert "Ошибка" in result

    @pytest.mark.parametrize("date_input,expected", [
        ("2023-01-01T12:00:00", "01.01.2023"),
        ("2024-12-31T23:59:59", "31.12.2024")
    ])
    def test_get_date_valid(self, date_input, expected):
        assert get_date(date_input) == expected

    def test_get_date_invalid_format(self):
        with pytest.raises(ValueError):
            get_date("некорректная_дата")