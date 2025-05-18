import json
import os
import re
import shutil
import time

import pyautogui
import pyperclip

prompt = """
英語の質問、参考情報、回答を日本語に翻訳し、次の厳密なフォーマットで1行のJSON（JSONL形式）として出力するGPTです：

1. 質問：自然で丁寧な日本語に翻訳。
2. 参考情報：英語の参考文を忠実に日本語へ翻訳。
3. 答え：
   - Chain-of-Thought（ステップバイステップ）形式で説明。
   - HTMLタグ（<p>、<ul>、<li>、<strong>など）を使用。
   - 各ステップに絵文字（例: 😊 ✅ 📄 🎤など）を含める。
   - 重要語句は<strong>タグ</strong>で強調。
   - 最後にまとめ文を<p>タグで記述し、✅マークを付ける。
   - リストが多い場合は3つごとに段落を分け、<br>などで読みやすく整形。

4. グラフ情報：
以下のグラフデータを使用して、答えに含めてください：
- **ノード**（例: "Visa_Student", "Doc_CoE"など）および**関係**（例: "Visa_Student requires_document Doc_CoE"など）を取り込み、回答に反映させる。
- もし質問の【参考情報】から関係性（例: "Visa_Student requires_document Doc_CoE"）を導き出すことができるなら、その情報をグラフデータとして生成してください。
- 【グラフ情報】は質問に関連する具体的な背景や構造的な情報を提供し、質問に対する回答に組み込むこと。

- グラフ情報は、テキスト情報を補完するために使用し、回答の正確性を向上させます。Graphを活用して具体的な関連情報を加える場合は、テキスト情報と組み合わせて統合してください。

例えば：
【参考情報】学生ビザを申請するためには、証明書（Certificate of Eligibility）が必要です。
→ 【グラフ情報】
{
  "ノード": [
    { "id": "Visa_Student", "label": "VisaType", "name": "学生ビザ" },
    { "id": "Doc_CoE", "label": "Document", "name": "証明書" }
  ],
  "関係": [
    { "source": "Visa_Student", "relation": "requires_document", "target": "Doc_CoE" }
  ]
}

不足があれば文脈から補完し、忠実かつ丁寧な日本語で自然な整形を行う。
"""

def copy(y):
    pyperclip.copy(f"Error: {filename}\n")
    pyautogui.moveTo(1230, y, duration=0.5)
    pyautogui.click()
    pyautogui.click()


def upload_file(is_first):
    pyautogui.moveTo(625, 850, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(700, 800, duration=0.5)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(650, 305, duration=0.5)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(1210, 680, duration=0.5)
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1320, 850, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1400, 850, duration=0.5)
    time.sleep(60)


def fill_first(is_first):
    # pyautogui.moveTo(180, 220, duration=0.5)
    # if is_first:
    #     pyautogui.click()
    # pyautogui.click()
    # time.sleep(10)

    # pyautogui.moveTo(180, 360, duration=0.5)
    # pyautogui.click()
    # time.sleep(10)

    pyautogui.moveTo(180, 160, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(180, 270, duration=0.5)
    pyautogui.click()
    time.sleep(10)

    # pyautogui.moveTo(650, 810, duration=0.5)
    # pyautogui.click()

    # pyautogui.hotkey("command", "a")
    # pyautogui.press("backspace")

    # pyperclip.copy(
    #     f'"""{prompt}"""\nYou must follow the prompt instructions and need to provide in jsonl format for the following questions'
    # )
    # pyautogui.hotkey("command", "v")

    # pyautogui.moveTo(1320, 850, duration=0.5)
    # pyautogui.click()
    # pyautogui.moveTo(1380, 850, duration=0.5)
    time.sleep(30)


def fill_file(filename, index=0):
    pyautogui.moveTo(635, 810, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    dest_path = os.path.join(destination_folder, filename)
    with open(dest_path, "r", encoding="utf-8") as file:
        content = json.load(file)
        num_rows = 10
        if index == 1:
            content = content[:5]
            num_rows = 5
        elif index == 2:
            content = content[5:]
            num_rows = 5
        data = f'"""\n{content}\n"""\nこのデータセット({filename}_{index}){num_rows}件を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を必ず日本語に翻訳し、グラフ情報を必ず参照して、必ずHTMLと絵文字を含むCoT形式の回答を生成してください。グラフ情報は必ず含めて出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。\n※答えにCoT形式をもっと詳しく入れてほしい\n※答えにもっと絵文字を入れてほしい\n※ノードの「name」を日本語に翻訳して欲しい'
        pyperclip.copy(data)
        pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1320, 850, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1400, 650, duration=0.5)
    time.sleep(120)


def is_valid_graph_info(graph_info):
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

    if not isinstance(graph_info["関係"], list):
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


def is_valid_format(obj):
    required_keys = {"質問", "参考情報", "答え"}

    if not isinstance(obj, dict):
        return False

    if not required_keys.issubset(obj.keys()):
        return False
    if not all(isinstance(obj[key], str) for key in required_keys):
        return False

    if "グラフ情報" not in obj:
        return False
    if not is_valid_graph_info(obj["グラフ情報"]):
        return False

    return True


def is_jsonl(lines):
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if not is_valid_format(obj):
                print(f"Invalid format in line {i}: {line}")
                return False
        except json.JSONDecodeError:
            return False
    return True

def replace_with_fallback(data):
    patterns = [(r"\n},\n{", "\n}\n\n{"), (r"\n}\n{", "\n}\n\n{")]
    for pattern, replacement in patterns:
        match = re.search(pattern, data, re.MULTILINE)
        if match:
            data = re.sub(pattern, replacement, data, flags=re.MULTILINE)
            break

    return data

examples_data = example_data = ['"グラフ情報":{"ノード":[{"id":"Visa_Student","label":"VisaType","name":"学生ビザ"},{"id":"Doc_CoE","label":"Document","name":"証明書"}],"関係":[{"source":"Visa_Student","relation":"requires_document","target":"Doc_CoE"}]}']

def append_data(filename, retry, index=0):
    pyautogui.scroll(-100)
    y_cors = [163,173,183,193,203,213,223,233,243,253, 263, 273, 283, 293, 303, 313,323,333,343,353,363, 373, 383, 393, 403, 413, 423, 433, 453, 463, 473]
    clipboard_data = ""
    num_rows = 0
    lines = []
    check_rows = 10 if index == 0 else 5
    for y_cor in y_cors:
        copy(y_cor)
        clipboard_data = pyperclip.paste()

        temp_lines = clipboard_data.strip().splitlines()

        if len(temp_lines) > 10:
            clipboard_data = replace_with_fallback(clipboard_data)
            clipboard_data = clipboard_data.strip().split("\n\n")

            clipboard_data = [json.loads(obj) for obj in clipboard_data]

            clipboard_data = "\n".join(
                json.dumps(obj, ensure_ascii=False) for obj in clipboard_data
            )
        else:
            clipboard_data = clipboard_data.replace("</p>\n<p>", "</p><p>")
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
            clipboard_data = "\n".join(clipboard_data)

        clipboard_data += "\n"

        if any(item in clipboard_data for item in example_data):
            num_rows = 0
            break

        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)

        if num_rows == check_rows:
            break

    is_appended = True
    if num_rows != check_rows or is_jsonl(lines) is False:
        clipboard_data = f"Error: {filename}, {num_rows}lines (index: {index})\n"
        is_appended = False
        if retry:
            return False

    with open("data/squad/translated.jsonl", "a", encoding="utf-8") as f:
        f.write(clipboard_data)

    return is_appended


def delete_temp_files():
    for filename in os.listdir(destination_folder):
        file_path = os.path.join(destination_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


def copy_file(filename):
    if os.path.isfile(source_path):
        dest_path = os.path.join(destination_folder, filename)
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")


def extract_number(filename):
    match = re.search(r"_(\d+)\.json$", filename)
    return int(match.group(1)) if match else -1


source_folder = "data/squad/processed/answers_chunks"
destination_folder = "temp/"


last = 4341
start = 4708
files = os.listdir(source_folder)
files = sorted(files, key=extract_number)[start:]
error_count = 0

is_first = True
count = 1
for filename in files:
    source_path = os.path.join(source_folder, filename)

    delete_temp_files()
    copy_file(filename)
    #upload_file(is_first, filename)v
    if count == 0:
        fill_first(is_first)

    # fill_file(filename)
    # is_appended = append_data(filename, True)
    is_appended = False
    if is_appended is False:
        for index in [1, 2]:
            fill_file(filename, index)
            is_appended = append_data(filename, False, index)
            if is_appended:
                error_count = 0
            else:
                error_count += 1

    pyautogui.moveTo(900, 850, duration=0.5)
    pyautogui.click()

    is_first = False
    count += 1
    if count >= 20:
        count = 0
        time.sleep(300)

    if error_count >= 5:
        break
