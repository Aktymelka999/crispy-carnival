from datetime import datetime


class BankWidget:
    def __init__(self, account_info: str, date_str: str):
        self.account_info = account_info
        self.date_str = date_str

    def render(self) -> str:
        masked = mask_account_card(self.account_info)
        formatted_date = get_date(self.date_str)
        return f"[Виджет] Карта/счёт: {masked}, Дата: {formatted_date}"


def mask_account_card(input_string: str) -> str:
    if not isinstance(input_string, str) or not input_string.strip():
        return ""

    parts = input_string.split()
    if len(parts) < 2:
        return input_string

    number = None
    for part in parts:
        if part.isdigit():
            number = part
            break

    if number is None:
        return input_string

    is_account = any(word.lower() in input_string.lower() for word in ["счёт", "account"])

    if is_account:
        masked = f"**{number[-4:]}"
    else:
        if len(number) >= 16:
            masked_core = "*" * (len(number) - 10)
            masked = f"{number[:6]}{masked_core}{number[-4:]}"
            formatted = []
            for i in range(0, len(masked), 4):
                formatted.append(masked[i : i + 4])
            masked = " ".join(formatted)
        else:
            masked = number

    return input_string.replace(number, masked, 1)


def get_date(date_string: str) -> str:
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_string, fmt)
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            continue
    raise ValueError("Некорректный формат даты")
