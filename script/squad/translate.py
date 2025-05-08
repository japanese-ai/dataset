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
    pyautogui.moveTo(180, 220, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(180, 360, duration=0.5)
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(650, 810, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    pyperclip.copy(
        f'"""{prompt}"""\nYou must follow the prompt instructions and need to provide in jsonl format for the following questions'
    )
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1320, 850, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1380, 850, duration=0.5)
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
        data = f'"""\n{content}\n"""\nFor {filename}_{index}, I want all {num_rows} rows in jsonl format'
        pyperclip.copy(data)
        pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1320, 850, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1400, 850, duration=0.5)
    time.sleep(180)


def is_valid_format(obj):
    required_keys = {"質問", "参考情報", "答え"}
    return (
        isinstance(obj, dict) and
        set(obj.keys()) == required_keys and
        all(isinstance(obj[key], str) for key in required_keys)
    )

def is_jsonl(lines):
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            if not is_valid_format(obj):
                return False
        except json.JSONDecodeError:
            return False
    return True


def append_data(filename, retry, index=0):
    y_cors = [263, 273, 283, 293, 303, 313,323,333,343,353,363, 373, 383, 393, 403, 413, 423, 433, 453, 463, 473]
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

    with open("data/squad/translated.jsonl", "a", encoding="utf-8") as f:
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


source_folder = "data/squad/processed/answers_chunks"
destination_folder = "temp/"


last = 4341
start = 2934
files = os.listdir(source_folder)
files = sorted(files, key=extract_number)[start:last]

is_first = True
count = 1
for filename in files:
    source_path = os.path.join(source_folder, filename)

    delete_temp_files()
    copy_file(filename)
    #upload_file(is_first, filename)v
    if count == 0:
        fill_first(is_first)

    fill_file(filename)
    is_appended = append_data(filename, True)

    if is_appended is False:
        for index in [1, 2]:
            fill_file(filename, index)
            append_data(filename, False, index)

    pyautogui.moveTo(900, 850, duration=0.5)
    pyautogui.click()

    is_first = False
    count += 1
    if count >= 100:
        count = 0
        # time.sleep(300)
        break
