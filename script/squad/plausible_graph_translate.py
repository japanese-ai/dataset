import json
import os
import re
import shutil
import time

import pyautogui
import pyperclip

prompt = """
英語の質問、参考情報、回答を日本語に翻訳し、以下の形式で1行のJSON（JSONL形式）として出力するGPTです：

【質問】自然で丁寧な日本語に翻訳。
【参考情報】意味を忠実に保って日本語へ翻訳。
【誤答候補】一見正しいが文書上でサポートされていない内容を日本語で記述。
【答え】以下の形式でHTMLを含めてCoTで出力：
- HTMLタグ（<p>, <ul>, <li>, <strong>など）を使用
- ステップごとに絵文字（😊 ✅ 📄 ⚠️ ❌ など）を加える
- plausible answer には ❌マークと理由を記述
- キーワードは<strong>で強調
- 最後に<p>まとめ文。</p>で締め、✅マークをつける
- 長いリストは3つごとに改行して整理する

【グラフ情報】以下のグラフデータを使用して、答えに含めてください：
- **ノード**（例: "Visa_Student", "Doc_CoE"など）および**関係**（例: "Visa_Student requires_document Doc_CoE"など）を取り込み、回答に反映させる。
- もし質問の【参考情報】から関係性（例: "Visa_Student requires_document Doc_CoE"）を導き出すことができるなら、その情報をグラフデータとして生成してください。
- 【グラフ情報】は質問に関連する具体的な背景や構造的な情報を提供し、質問に対する回答に組み込むこと。

グラフ情報は、テキスト情報を補完するために使用し、回答の正確性を向上させます。Graphを活用して具体的な関連情報を加える場合は、テキスト情報と組み合わせて統合してください。

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
"""


def copy(y):
    pyperclip.copy(f"Error: {filename}\n")
    pyautogui.moveTo(950, y, duration=0.5)
    pyautogui.click()
    pyautogui.click()


def upload_file(is_first):
    pyautogui.moveTo(460, 880, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(500, 840, duration=0.5)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(1000, 320, duration=0.5)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(1120, 710, duration=0.5)
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1030, 890, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1100, 890, duration=0.5)
    time.sleep(90)


def fill_first(is_first):
    pyautogui.moveTo(180, 230, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(180, 340, duration=0.5)
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(470, 840, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    pyperclip.copy(
        f'"""{prompt}"""\nYou must follow the prompt instructions and need to provide in jsonl format for the following questions'
    )
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1040, 880, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1100, 880, duration=0.5)
    time.sleep(30)


def fill_file(filename, index=0):
    pyautogui.moveTo(470, 840, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    dest_path = os.path.join(destination_folder, filename)
    num_rows = 10 if index == 0 else 5
    with open(dest_path, "r", encoding="utf-8") as file:
        content = json.load(file)
        if index == 1:
            content = content[:5]
        elif index == 2:
            content = content[5:]
        data = f'"""\n{content}\n"""\nこのデータセット({filename}_{index})を、指定されたプロンプトに従って変換してください。具体的には、質問と参考情報を日本語に翻訳し、グラフ情報を必ず参照して、HTMLを含むCoT形式の回答を生成してください。グラフ情報は必ず含め、誤答候補も出力してください。出力はJSONL形式でお願いします。出力は各データが1行として全て{num_rows}件とも表示されるようにしてください。'
        pyperclip.copy(data)
        pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1040, 880, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1100, 880, duration=0.5)
    time.sleep(180)


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
    required_keys = {"質問", "参考情報", "誤答候補", "答え"}

    if not isinstance(obj, dict):
        return False

    if not required_keys.issubset(obj.keys()):
        return False
    if not all(isinstance(obj[key], str) for key in required_keys):
        return False

    if "グラフ情報" in obj:
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


def append_data(filename, retry, index=0):
    y_cors = [
        287,
        297,
        307,
        317,
        327,
        337,
        347,
        357,
        367,
        377,
        387,
        397,
        407,
        417,
        427,
        437,
        447,
        457,
        467,
        477,
    ]
    clipboard_data = ""
    num_rows = 0
    lines = []
    check_rows = 10 if index == 0 else 5
    for y_cor in y_cors:
        copy(y_cor)
        clipboard_data = pyperclip.paste()
        clipboard_data = "\n".join(
            [line for line in clipboard_data.split("\n") if line.strip()]
        )
        clipboard_data += "\n"
        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)

        if num_rows == check_rows:
            break

    if num_rows != check_rows or is_jsonl(lines) is False:
        clipboard_data = f"Error: {filename}, {num_rows}lines (index: {index})\n"
        if retry:
            return False

    with open("data/squad/plausible_translated.jsonl", "a", encoding="utf-8") as f:
        f.write(clipboard_data)

    return True


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


source_folder = "data/squad/processed/plausible_chunks"
destination_folder = "temp/"


last = 2174
start = 2175
files = os.listdir(source_folder)
files = sorted(files, key=extract_number)[start:]
is_first = True
count = 1
for filename in files:
    source_path = os.path.join(source_folder, filename)

    delete_temp_files()
    copy_file(filename)
    # upload_file(is_first, filename)
    if count == 0:
        fill_first(is_first)

    # fill_file(filename)
    # is_appended = append_data(filename, True)
    is_appended = False

    if is_appended is False:
        for index in [1, 2]:
            fill_file(filename, index)
            append_data(filename, False, index)

    pyautogui.moveTo(660, 890, duration=0.5)
    pyautogui.click()

    is_first = False

    count += 1
    if count >= 100:
        count = 0
        break
        # time.sleep(300)
