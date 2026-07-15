import pytest

from src.widget import get_date, mask_account_card  # импорт get_date добавлен


class TestWidgetFunctions:
    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("Счёт 12345678901234567890", "Счёт **7890"),
            ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
            ("", ""),  # пустая строка → пустая строка
            ("Без номера", "Без номера"),
        ],
    )
    def test_mask_account_card_valid(self, input_str, expected):
        assert mask_account_card(input_str) == expected

    def test_mask_account_card_empty_input(self):
        result = mask_account_card("")
        assert result == ""  # исправлено: ожидаем пустую строку

    @pytest.mark.parametrize(
        "date_input,expected", [("2023-01-01T12:00:00", "01.01.2023"), ("2024-12-31T23:59:59", "31.12.2024")]
    )
    def test_get_date_valid(self, date_input, expected):
        assert get_date(date_input) == expected  # get_date теперь доступен

    def test_get_date_invalid_format(self):
        with pytest.raises(ValueError):
            get_date("некорректная_дата")  # get_date теперь доступен


#def test_mask_account_card():
    #test_cases = [
        #("Maestro 1596837868705199", "Maestro 159683**68705199"),  # пример под твою логику
        #("Счет 64686473678894779589", "Счет **9589"),
        #("MasterCard 7158300734726758", "MasterCard 715830**34726758"),
        #("Visa 4111111111111111", "Visa 411111**11111111"),
        #("Карта 1234567812345678", "Карта 123456**12345678"),
        #("1234567890123456", "123456**90123456"),
        #("МИР 2200700567891234", "МИР 220070**67891234"),
    #]

    #for inp, expected in test_cases:
        #assert mask_account_card(inp) == expected, f"Failed for input: {inp!r}"


def test_get_date():
    date_str = "2024-03-11T02:26:18.671407"
    result = get_date(date_str)
    assert result == "11.03.2024"
