Описание
Проект project.py реализует бэкенд‑логику для нового виджета в личном кабинете клиента банка. Виджет показывает:

дату и время операции;

тип операции (перевод, оплата, пополнение и т. д.);

сумму операции (с указанием валюты);

получателя/отправителя (короткий идентификатор);

статус операции (гарантированно «успешно»).

Технологии
Язык программирования: Python 3.14;

Веб‑фреймворк: Flask (лёгковесный сервер для API);

База данных: SQLite (для демонстрации; в продакшене — PostgreSQL/Oracle);

Форматы данных: JSON (обмен между бэкендом и фронтендом).

Установка
Убедитесь, что установлен Python 3.14.

Клонируйте репозиторий:

git clone [ https://github.com/Aktymelka999/crispy-carnival.git]
cd Widget-Bank-Operations
Установите зависимости:

pip install -r requirements.txt

Запустите приложение:

python project.py

Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).
Контактная информация
По вопросам, связанным с проектом, обращайтесь:

Email: gertrudadeputat35@gmail.com

GitHub: [ https://github.com/Aktymelka999/crispy-carnival.git]


## Тестирование:
Цель тестирования — проверить корректность работы всех функций проекта и выявить ошибки.

###Процесс тестирования
- PyTest — для написания и запуска тестов.
- Coverage.py — для измерения покрытия кода тестами.
- Статические анализаторы (Flake8, mypy) — для проверки кода.

# Установка зависимостей для тестирования
pip install -r requirements-test.txt

# Запуск тестов с PyTest
pytest

# Запуск с измерением покрытия кода
coverage run -m pytest
coverage report

###Ключевые тестовые сценарии:
корректность работы функции mask_account_card с разными входными данными;
преобразование даты в функции get_date;
фильтрация транзакций в filter_by_state;
сортировка транзакций в sort_by_date;
работа метода show_executed в классе Widget.

# Новый модуль: src.generators.data_generators
Модуль предоставляет утилиты для обработки и генерации данных транзакций. Предназначен для использования в тестировании и предварительной обработке данных.

Список функций:

filter_by_currency(transactions, currency)
Фильтрует список транзакций по указанной валюте.

Параметры:

transactions — список словарей с данными транзакций;

currency — строка с названием валюты (например, "USD", "RUB").

Возвращает: генератор отфильтрованных транзакций.

transaction_descriptions(transactions)
Извлекает описания транзакций из списка.

Параметр: transactions — список словарей с данными транзакций.

Возвращает: генератор строк с описаниями ("description" из каждого словаря).

card_number_generator(start, end)
Генерирует последовательность номеров карт в формате XXXX XXXX XXXX XXXX.

Параметры:

start — начальное 16‑значное число;

end — конечное 16‑значное число.

Возвращает: генератор отформатированных номеров карт.

Примеры использования
Пример 1. Фильтрация транзакций по валюте (USD)
from src.generators.data_generators import filter_by_currency

 Используем предоставленные данные transactions
usd_transactions = list(filter_by_currency(transactions, "USD"))

print(f"Найдено транзакций в USD: {len(usd_transactions)}")
for tx in usd_transactions:
    print(f"ID: {tx['id']}, Сумма: {tx['operationAmount']['amount']} {tx['operationAmount']['currency']['name']}, Описание: {tx['description']}")
    Выврд:
    Найдено транзакций в USD: 3
ID: 939719570, Сумма: 9824.07 USD, Описание: Перевод организации
ID: 142264268, Сумма: 79114.93 USD, Описание: Перевод со счёта на счёт
ID: 895315941, Сумма: 56883.54 USD, Описание: Перевод с карты на карту

Пример 2. Извлечение описаний транзакций
from src.generators.data_generators import transaction_descriptions

descriptions = list(transaction_descriptions(transactions))

print("Описания транзакций:")
for desc in descriptions:
    print(desc)

    Вывод:
      Описания транзакций:
Перевод организации
Перевод со счёта на счёт
Перевод со счёта на счёт
Перевод с карты на карту
Перевод организации

Пример 3. Генерация номеров карт
from src.generators.data_generators import card_number_generator

 Генерируем 3 номера карт начиная с 1111222233334444
cards = card_number_generator(1111222233334444, 1111222233334446)

for card in cards:
    print(card)
    Вывод:
1111 2222 3333 4444
1111 2222 3333 4445
1111 2222 3333 4446

Входные данные для тестирования
Для проверки функций используйте следующий список транзакций:
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "Счёт 75106830613657916952",
        "to": "Счёт 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод со счёта на счёт",
        "from": "Счёт 19708645243227258542",
        "to": "Счёт 75651667383060284188"
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод со счёта на счёт",
        "from": "Счёт 44812258784861134719",
        "to": "Счёт 74489636417521191160"
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229"
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"}
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счёт 14211924144426031657"
    }
]