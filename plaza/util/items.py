import json
from pathlib import Path

from ..types import CategoryTypes

pwd = Path(__file__).parent

with open(pwd / "item_db.json") as f:
    item_db: dict[int, dict[str, str | int | CategoryTypes]] = {
        int(k): v | {"expected_category": CategoryTypes(v["expected_category"])}
        for k, v in json.loads(f.read())
    }

VALID_ITEMS = list(item_db.keys())
