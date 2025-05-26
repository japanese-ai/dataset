import json
import re
import time

import pyautogui
import pyperclip

from script.util import (
    has_duplicate_emojis,
    has_html_tags,
    has_japanese,
    has_only_one_unique_emoji,
    is_valid_graph_info,
)

example_data = [
    '"グラフ情報":{"ノード":[{"id":"Visa_Student","label":"VisaType","name":"学生ビザ"},{"id":"Doc_CoE","label":"Document","name":"証明書"}],"関係":[{"source":"Visa_Student","relation":"requires_document","target":"Doc_CoE"}]}'
]


def make_new_chat(is_first):
    pyautogui.moveTo(180, 180, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(180, 360, duration=0.5)
    pyautogui.click()
    time.sleep(30)


def fill_file(data):
    pyautogui.moveTo(470, 840, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    data = f'"""\n{data}\n"""\n一行づつの答えにCoT形式をもっと詳しく入れて欲しい。出力はJSONL形式でお願いします。出力は各データが1行として全て5件とも表示されるようにしてください。\n※「no」項目とグラフ情報の出力は忘れずに\n※誤答候補を日本語に翻訳するのを忘れずに'
    pyperclip.copy(data)
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1040, 880, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1100, 680, duration=0.5)
    time.sleep(120)


def copy(batch_no_list, y_cor):
    pyperclip.copy(f"Error: {batch_no_list}\n")
    pyautogui.moveTo(950, y_cor, duration=0.5)
    pyautogui.click()
    pyautogui.click()


def replace_with_fallback(data):
    patterns = [
        (r"\n},\n{", "\n}\n\n{"),
        (r"\n}\n{", "\n}\n\n{"),
        (r"\n]}}", "\n]}}\n\n"),
    ]
    for pattern, replacement in patterns:
        match = re.search(pattern, data, re.MULTILINE)
        if match:
            data = re.sub(pattern, replacement, data, flags=re.MULTILINE)
            break

    return data


def get_clipboard_data(clipboard_data):
    clipboard_data = clipboard_data.replace("</p>\n<p>", "</p><p>")
    clipboard_data = clipboard_data.replace("</li>\n  <li>", "</li><li>")
    clipboard_data = clipboard_data.replace("</li>\n<li>", "</li><li>")
    clipboard_data = clipboard_data.replace("\n<ul>\n  ", "<ul>")
    clipboard_data = clipboard_data.replace("\n</ul>\n", "</ul>")

    temp_lines = clipboard_data.strip().splitlines()

    if len(temp_lines) > 20:
        clipboard_data = replace_with_fallback(clipboard_data)
        clipboard_data = clipboard_data.strip().split("\n\n")
    else:
        clipboard_data = [
            line
            for line in clipboard_data.strip().splitlines()
            if line not in ["", "}", ",", "},"]
        ]
        clipboard_data = [
            (
                line.strip() + ("}" if line.strip().endswith("}]}") else "")
                if not line.endswith("}]}}")
                else line
            )
            for line in clipboard_data
        ]
        clipboard_data = [(line.replace("}]}},", "}]}}")) for line in clipboard_data]

    try:
        clipboard_data = [json.loads(obj) for obj in clipboard_data]
        clipboard_data = [json.dumps(obj, ensure_ascii=False) for obj in clipboard_data]
        clipboard_data = "\n".join(clipboard_data)
        clipboard_data += "\n"
    except Exception:
        return False, 0, None, None

    if any(item in clipboard_data for item in example_data):
        return True, 0, None, None

    lines = clipboard_data.strip().splitlines()
    num_rows = len(lines)

    if num_rows == 5:
        return True, num_rows, clipboard_data, lines

    return False, 0, None, None


def is_valid_format(obj):
    required_keys = {"質問", "参考情報", "誤答候補", "答え"}

    if not isinstance(obj, dict):
        return False

    if not required_keys.issubset(obj.keys()):
        return False

    if not all(isinstance(obj[key], str) for key in required_keys):
        return False

    if (
        has_only_one_unique_emoji(obj.get("答え"))
        or has_duplicate_emojis(obj.get("答え"))
        or not has_html_tags(obj.get("答え"))
    ):
        return False

    for key in required_keys:
        if not has_japanese(obj.get(key)):
            return False

    if "グラフ情報" not in obj:
        return False

    if not is_valid_graph_info(obj["グラフ情報"]):
        return False

    return True


def is_jsonl(lines, batch_no_list):
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if not is_valid_format(obj):
                return False
            if obj.get("no") not in batch_no_list:
                return False
        except json.JSONDecodeError:
            return False
    return True


def append_data(batch, batch_no_list):
    pyautogui.scroll(-100)
    y_cors = list(range(177, 588, 10))

    clipboard_data = ""
    num_rows = 0
    lines = []
    for y_cor in y_cors:
        copy(batch_no_list, y_cor)
        clipboard_data = pyperclip.paste()
        got_data, num_rows, clipboard_data, lines = get_clipboard_data(clipboard_data)

        if got_data:
            break

    is_appended = True
    if num_rows != 5 or is_jsonl(lines, batch_no_list) is False:
        clipboard_data = f"Error: {batch_no_list}\n\n\n\n\n"
        is_appended = False

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(clipboard_data)

    return is_appended


input_file = "data/squad/plausible_translated_answer.jsonl"
output_file = "data/squad/plausible_translated_answer_fixed.jsonl"

# read file
with open(input_file, "r", encoding="utf-8") as f:
    data_list = [json.loads(line) for line in f]

start = 1145
count = 1
error_count = 0
data_list = data_list[start:]
batch_size = 5
is_first = True


for i in range(0, len(data_list), batch_size):
    data = data_list[i : i + batch_size]

    if count == 0:
        make_new_chat(is_first)

    fill_file(data)
    no_list = [item["no"] for item in data]

    is_appended = append_data(data, no_list)
    if is_appended is True:
        error_count = 0
    else:
        error_count += 1

    pyautogui.moveTo(660, 890, duration=0.5)
    pyautogui.click()

    is_first = False

    count += 1
    if count > 30:
        count = 0
        time.sleep(300)

    if error_count >= 5:
        break
