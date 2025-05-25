import json
import re

import emoji


def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]


def has_only_one_unique_emoji(text):
    emojis = extract_emojis(text)
    return len(emojis) == 1


def has_duplicate_emojis(text):
    emojis = extract_emojis(text)
    return len(emojis) > 1 and len(set(emojis)) == 1


def has_html_tags(text):
    return bool(re.search(r"<[^>]+>", text))


KEY_TO_CHECK = "答え"

input_file = "data/squad/plausible_translated.jsonl"
output_file = "data/squad/plausible_translated_answer.jsonl"

filtered_data = []

with open(input_file, "r") as infile:
    for line in infile:
        obj = json.loads(line)
        text = obj.get(KEY_TO_CHECK, "")

        if (
            has_only_one_unique_emoji(text)
            or has_duplicate_emojis(text)
            or not has_html_tags(text)
        ):
            filtered_data.append(obj)

print(f"Length: {len(filtered_data)}")
with open(output_file, "w", encoding="utf-8") as out:
    for item in filtered_data:
        out.write(json.dumps(item, ensure_ascii=False) + "\n")
