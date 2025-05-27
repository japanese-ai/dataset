import json

input_file = "data/squad/plausible_translated_answer.jsonl"
output_file = "data/squad/plausible_translated_answer_fixed.jsonl"


with open(input_file, "r", encoding="utf-8") as f:
    org_data_list = [json.loads(line) for line in f]
    org_data_list = [item["no"] for item in org_data_list]


with open(output_file, "r", encoding="utf-8") as f:
    fix_data_list = [json.loads(line) for line in f]
    fix_data_list = [item["no"] for item in fix_data_list]


missing_items = [item for item in org_data_list if item not in fix_data_list]
result = len(missing_items) == 0
print(f"All items in the original data are present in the fixed data: {result}")
if not result:
    print(f"Missing items: {missing_items}")
