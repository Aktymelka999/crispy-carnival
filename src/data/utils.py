import json
from pathlib import Path
from typing import List, Dict, Any

def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.

    Возвращает пустой список, если:
      - файл не найден;
      - содержимое не является JSON;
      - JSON не является списком;
      - список пуст.

    :param file_path: путь к JSON-файлу (может быть относительным или абсолютным)
    :return: список словарей с транзакциями или пустой список при ошибках
    """
    path = Path(file_path)

    # Проверка существования файла
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        # JSON невалиден или ошибка чтения файла 
        return []

    # Проверяем, что данные — это список
    if not isinstance(data, list):
        return []

    return data