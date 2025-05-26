import re

import emoji


def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]


def has_only_one_unique_emoji(text):
    emojis = extract_emojis(text)
    if len(emojis) == 1:
        return True


def has_duplicate_emojis(text):
    emojis = extract_emojis(text)
    return len(emojis) > 1 and len(set(emojis)) == 1


def has_html_tags(text):
    return bool(re.search(r"<[^>]+>", text))


def has_japanese(text):
    # Match Japanese characters
    japanese_pattern = re.compile(
        r"[\u3040-\u30ff\u4e00-\u9fff\u30a0-\u30ff\uff66-\uff9f]"
    )

    # Match a number followed by % (e.g., 2.5%, 100%, 0%)
    percentage_pattern = re.compile(r"\b\d+(\.\d+)?%")

    return bool(
        re.search(japanese_pattern, text) or re.search(percentage_pattern, text)
    )


def is_valid_graph_info(graph_info, obj, require_keys):
    if not isinstance(graph_info, dict):
        return False

    if not all(key in graph_info for key in ["ノード", "関係"]):
        return False

    if not isinstance(graph_info["ノード"], list):
        return False
    for node in graph_info["ノード"]:
        if not isinstance(node, dict):
            return False
        if not all(key in node for key in ["id", "label", "name"]):
            return False
        if not all(isinstance(node[key], str) for key in ["id", "label", "name"]):
            return False
        for key in require_keys:
            if not obj.get(key).contains(node.get("name")):
                return False

    if not isinstance(graph_info["関係"], list):
        return False
    if len(graph_info["関係"]) == 0:
        return False
    for relation in graph_info["関係"]:
        if not isinstance(relation, dict):
            return False
        if not all(key in relation for key in ["source", "relation", "target"]):
            return False
        if not all(
            isinstance(relation[key], str) for key in ["source", "relation", "target"]
        ):
            return False

    return True
