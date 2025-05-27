import json
import os
from collections import OrderedDict
from pathlib import Path


def format_and_split(input_path: str, output_path: str):
    # Delete existing output files if present
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"🗑️ Deleted: {output_path}")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    # Read raw file
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    with open(output_path, "w", encoding="utf-8") as out:
        for idx, obj in enumerate(raw_data):
            new_obj = OrderedDict()
            new_obj["no"] = idx + 1
            for k, v in obj.items():
                new_obj[k] = v

            json.dump(new_obj, out, ensure_ascii=False)
            out.write("\n")

    print(f"✅ Saved {output_path}")


# Usage
format_and_split(
    input_path="data/alpaca/raw/alpaca_data.json",
    output_path="data/alpaca/processed/alpaca_data.jsonl",
)
