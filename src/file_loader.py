import json
from pathlib import Path
from typing import List, Dict, Any
from decimal import Decimal

def load_transactions(file_path: str | Path) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Опционально: сразу конвертируем суммы в Decimal для точности
    for tx in data:
        if "amount" in tx:
            tx["amount"] = Decimal(str(tx["amount"]))

    return data