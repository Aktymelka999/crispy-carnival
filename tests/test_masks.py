import pytest
from src.masks import mask_card_number, mask_account_number

class TestMasks:
    @pytest.mark.parametrize("card_num,expected", [
        ("1234567890123456", "1234 56** **** 3456"),
        ("4444333322221111", "4444 33** **** 1111")
    ])
    def test_mask_card_number_valid(self, card_num, expected):
        assert mask_card_number(card_num) == expected


    @pytest.mark.parametrize("invalid_card", [
        "123456789012",  # слишком короткий
        "12345678901234567890",  # слишком длинный
        "123a567b901c345d",  # не цифры
        ""  # пустая строка
    ])
    def test_mask_card_number_invalid(self, invalid_card):
        with pytest.raises(ValueError):
            mask_card_number(invalid_card)

    @pytest.mark.parametrize("account_num,expected", [
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210")
    ])
    def test_mask_account_number_valid(self, account_num, expected):
        assert mask_account_number(account_num) == expected

    @pytest.mark.parametrize("invalid_account", [
        "123456789012",
        "123456789012345678901234",
        "123a567b901c345d678e",
        ""
    ])
    def test_mask_account_number_invalid(self, invalid_account):
        with pytest.raises(ValueError):
            mask_account_number(invalid_account)