import json

input_file = "data/squad/plausible_translated_related_merged.jsonl"
output_file = "data/squad/plausible_translated_related.jsonl"

filtered_data = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        if "グラフ情報" in obj and obj.get("グラフ情報").get("関係") == []:
            filtered_data.append(obj)

print(f"Length: {len(filtered_data)}")
# with open(output_file, "w", encoding="utf-8") as out:
#     for item in filtered_data:
#         out.write(json.dumps(item, ensure_ascii=False) + "\n")
