import json

input_file = "data/squad/plausible_translated_related.jsonl"
output_file = "data/squad/plausible_translated_related_fixed.jsonl"


with open(input_file, "r", encoding="utf-8") as f:
    org_data_list = [json.loads(line) for line in f]
    org_data_list = [item["no"] for item in org_data_list]


with open(output_file, "r", encoding="utf-8") as f:
    fix_data_list = [json.loads(line) for line in f]
    fix_data_list = [item["no"] for item in fix_data_list]


result = all(item in fix_data_list for item in org_data_list)

print(result)
