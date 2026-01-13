import json
from pathlib import Path


ENUM_PATH = Path(__file__).parent / "enums.json"

with open(ENUM_PATH, "r", encoding="utf-8") as f:
    OPERATIONS = json.load(f)

if "CREATE" in OPERATIONS.keys():
    print(True)

