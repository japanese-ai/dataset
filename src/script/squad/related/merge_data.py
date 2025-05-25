import json

merged = {}

original_file = "data/squad/plausible_translated.jsonl"
fixed_file = "data/squad/plausible_translated_related_fixed.jsonl"
mrrged_file = "data/squad/plausible_translated_related_merged.jsonl"

with open(original_file, "r") as f1:
    for line in f1:
        obj = json.loads(line)
        merged[obj["no"]] = obj

with open(fixed_file, "r") as f2:
    for line in f2:
        obj = json.loads(line)
        merged[obj["no"]] = obj

# Write merged results
with open(mrrged_file, "w") as out:
    for obj in merged.values():
        out.write(json.dumps(obj, ensure_ascii=False) + "\n")
