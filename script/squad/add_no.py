import json
from collections import OrderedDict

input_file = "data/squad/plausible_translated.jsonl"
output_file = "data/squad/plausible_translated_1.jsonl"

fixed_data = []

with open(input_file, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        line = line.strip()
        if not line:
            continue

        data = json.loads(line)

        # Insert 'id' at the beginning using OrderedDict
        new_obj = OrderedDict()
        new_obj["no"] = idx + 1
        for k, v in data.items():
            new_obj[k] = v

        fixed_data.append(new_obj)

with open(output_file, "w", encoding="utf-8") as f:
    for item in fixed_data:
        json.dump(item, f, ensure_ascii=False)
        f.write("\n")
