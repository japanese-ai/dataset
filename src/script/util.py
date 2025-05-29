import re

import emoji


def extract_emojis(text):
    return [char for char in text if char in emoji.EMOJI_DATA]


def has_more_than_one_emoji(text, is_cot):
    emojis = extract_emojis(text)
    if is_cot:
        return len(emojis) > 1

    return True


def has_duplicate_emojis(text):
    emojis = extract_emojis(text)
    return len(emojis) > 1 and len(set(emojis)) == 1


def has_html_tags(text):
    return bool(re.search(r"<[^>]+>", text))


def remove_html_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def has_japanese(text):
    # Match Japanese characters
    japanese_pattern = re.compile(
        r"[\u3040-\u30ff\u4e00-\u9fff\u30a0-\u30ff\uff66-\uff9f]"
    )

    # Match a number followed by % (e.g., 2.5%, 100%, 0%)
    percentage_pattern = re.compile(r"\b\d+(\.\d+)?%")

    # Match Python-style list: e.g., x = [1, 2, 3]
    list_pattern = re.compile(r"\w+\s*=\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\]")

    return bool(
        re.search(japanese_pattern, text)
        or re.search(percentage_pattern, text)
        or re.search(list_pattern, text)
    )


def is_valid_answer(answer, is_cot=True):

    if not has_more_than_one_emoji(answer, is_cot):
        return False, "Only have one emoji"

    if has_duplicate_emojis(answer):
        return False, "Has duplicate emojis in the answer"

    if not has_html_tags(answer):
        return False, "Answer does not contain HTML tags"

    if is_cot:
        has_icons_or_tags = bool(
            re.search(
                r"[🔬📄✅🧲📘📚📝⚠️❓➡️💡]|<strong>|<p>|<ol>|<ul>|<li>|<em>", answer
            )
        )

        if not has_icons_or_tags:
            return False, "Answer does not contain CoT icons or tags"

    return True, ""


def is_valid_graph_info(graph_info, allow_empty_data=False):
    if not isinstance(graph_info, dict):
        return (
            False,
            f"Invalid type: Expected a dictionary, got {type(graph_info).__name__}",
        )

    if not all(key in graph_info for key in ["ノード", "関係"]):
        return (
            False,
            f"Missing required keys: {set(['ノード', '関係']) - set(graph_info.keys())}",
        )

    if not isinstance(graph_info["ノード"], list):
        return False, "ノード must be a list"

    if len(graph_info["ノード"]) == 0 and not allow_empty_data:
        return False, "ノード list cannot be empty"

    for node in graph_info["ノード"]:
        if not isinstance(node, dict):
            return (
                False,
                f"Invalid type for ノード item: Expected a dictionary, got {type(node).__name__}",
            )

        if not all(key in node for key in ["id", "label", "name"]):
            return (
                False,
                f"Missing required keys in ノード item: {set(['id', 'label', 'name']) - set(node.keys())}",
            )

        if not all(isinstance(node[key], str) for key in ["id", "label", "name"]):
            return False, "All ノード keys must have string values"

    if not isinstance(graph_info["関係"], list):
        return False, "関係 must be a list"

    if len(graph_info["関係"]) == 0 and not allow_empty_data:
        return False, "関係 list cannot be empty"

    for relation in graph_info["関係"]:
        if not isinstance(relation, dict):
            return (
                False,
                f"Invalid type for 関係 item: Expected a dictionary, got {type(relation).__name__}",
            )

        if not all(key in relation for key in ["source", "relation", "target"]):
            return (
                False,
                f"Missing required keys in 関係 item: {set(['source', 'relation', 'target']) - set(relation.keys())}",
            )

        if not all(
            isinstance(relation[key], str) for key in ["source", "relation", "target"]
        ):
            return False, "All 関係 keys must have string values"

    return True, ""
