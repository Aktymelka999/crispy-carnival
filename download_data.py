
import requests
from pathlib import Path

URLS = {
    "transactions.csv": "https://raw.githubusercontent.com/skypro-008/transactions/main/transactions.csv",
    "transactions_excel.xlsx": "https://raw.githubusercontent.com/skypro-008/transactions/main/transactions_excel.xlsx",
}

PROJECT_ROOT = Path(__file__).parent


def download_file(url: str, filename: str):
    print(f"📥 Скачиваю {filename}...")
    try:

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        file_path = PROJECT_ROOT / filename
        file_path.write_bytes(response.content)
        print(f"✅ Файл сохранён: {file_path}")
        return True
    except requests.exceptions.Timeout:
        print(f"❌ Ошибка: скачивание {filename} заняло слишком много времени (превышен таймаут).")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP-ошибка при скачивании {filename}: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка при скачивании {filename}: {e}")
        return False


if __name__ == "__main__":
    success_count = 0
    for filename, url in URLS.items():
        if download_file(url, filename):
            success_count += 1

    print("-" * 30)
    if success_count == len(URLS):
        print("🎉 Все файлы скачаны!")
        print("⚠️ Обязательно проверь transactions.csv в Блокноте:")
        print("   1. Разделитель — точка с запятой (;)")
        print("   2. Первая строка — id;currency;amount;description;date;state")
    else:
        print("⚠️ Скачались не все файлы.")
        print("💡 Для Excel лучше используй make_excel.py — он создаст гарантированно рабочий файл.")
