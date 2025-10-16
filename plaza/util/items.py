import json
from pathlib import Path

pwd = Path(__file__).parent

with open(pwd / "item_db.json") as f:
    item_db: dict[int, dict[str, str | int]] = json.loads(f.read())

VALID_ITEMS = list(item_db.keys())
