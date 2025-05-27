import json

original_file = "data/squad/plausible_translated.jsonl"
fixed_file = "data/squad/plausible_translated_answer_fixed.jsonl"
mrrged_file = "data/squad/plausible_translated_answer_merged.jsonl"

merged = {}

with open(original_file, "r") as f1:
    for line in f1:
        obj = json.loads(line)
        merged[obj["no"]] = obj

with open(fixed_file, "r") as f2:
    for line in f2:
        obj = json.loads(line)
        no = obj["no"]
        if no in merged:
            new_obj = {}
            for key in merged[no]:
                new_obj[key] = obj.get(key, merged[no][key])
            merged[no] = new_obj

# Write merged results
with open(mrrged_file, "w") as out:
    for obj in merged.values():
        out.write(json.dumps(obj, ensure_ascii=False) + "\n")
