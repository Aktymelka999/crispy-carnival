import pytest
from masks import get_mask_card_number, get_mask_account


class TestGetMaskCardNumber:
    @pytest.mark.parametrize("card_number,expected", [
        # Стандартные 16‑значные карты
        ("1234567890123456", "1234 56** **** 3456"),
        ("4444333322221111", "4444 33** **** 1111"),
        # Карты с пробелами
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        # Карты с дефисами
        ("1234-5678-9012-3456", "1234 56** **** 3456"),
        # Американ Экспресс (15 цифр)
        ("378282246310005", "3782 82** **** 005"),
    ])
    def test_valid_card_numbers(self, card_number, expected):
        """Тест корректного маскирования номеров карт разных форматов."""
        result = get_mask_card_number(card_number)
        assert result == expected

    @pytest.mark.parametrize("invalid_card,expected_error", [
        ("", "Invalid card number"),
        ("123", "Invalid card number"),  # Слишком короткий
        ("1" * 20, "Invalid card number"),  # Слишком длинный
        ("abcdefghijklmnop", "Invalid card number"),  # Буквы вместо цифр
        (None, "Invalid card number"),  # None
    ])
    def test_invalid_card_numbers(self, invalid_card, expected_error):
        """Тест обработки некорректных входных данных."""
        with pytest.raises(ValueError, match=expected_error):
            get_mask_card_number(invalid_card)

    def test_no_card_in_string(self):
        """Тест когда входная строка не содержит номера карты."""
        with pytest.raises(ValueError, match="Invalid card number"):
            get_mask_card_number("No card here")


class TestGetMaskAccount:
    @pytest.mark.parametrize("account_number,expected", [
        # Стандартный номер счёта (20 цифр)
        ("12345678901234567890", "**7890"),
        # С пробелами
        ("1234 5678 9012 3456 7890", "**7890"),
        # С дефисами
        ("1234-5678-9012-3456-7890", "**7890"),
    ])
    def test_valid_account_numbers(self, account_number, expected):
        """Тест корректного маскирования номеров счетов."""
        result = get_mask_account(account_number)
        assert result == expected

    @pytest.mark.parametrize("short_account,expected", [
        ("123", "**123"),  # Очень короткий
        ("1234", "**1234"),  # Короткий
        ("12", "**12"),  # Минимально возможный
    ])
    def test_short_account_numbers(self, short_account, expected):
        """Тест для номеров счетов короче ожидаемой длины."""
        result = get_mask_account(short_account)
        assert result == expected

    @pytest.mark.parametrize("invalid_account,expected_error", [
        ("", "Invalid account number"),
        ("abc", "Invalid account number"),  # Буквы
        (None, "Invalid account number"),  # None
    ])
    def test_invalid_account_numbers(self, invalid_account, expected_error):
        """Тест обработки некорректных номеров счетов."""
        with pytest.raises(ValueError, match=expected_error):
            get_mask_account(invalid_account)