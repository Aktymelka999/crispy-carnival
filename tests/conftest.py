import os
import sys
import pytest

# Получаем путь к директории tests
tests_dir = os.path.dirname(__file__)
# Поднимаемся на уровень вверх (к корневой директории проекта) и добавляем src
src_path = os.path.abspath(os.path.join(tests_dir, "../src"))
# Добавляем путь в начало sys.path
if src_path not in sys.path:
    sys.path.insert(0, src_path)


@pytest.fixture
def empty_transactions():
    """Фикстура для пустого списка транзакций."""
    return []
