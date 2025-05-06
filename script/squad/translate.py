import json
import os
import re
import shutil
import time

import pyautogui
import pyperclip

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
    pyautogui.moveTo(180, 150, duration=0.5)
    if is_first:
        pyautogui.click()
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(180, 260, duration=0.5)
    pyautogui.click()
    time.sleep(10)

    pyautogui.moveTo(650, 610, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    pyperclip.copy(
        "You must follow the prompt instructions and need to provide in jsonl format for the following questions"
    )
    pyautogui.hotkey("command", "v")

    pyautogui.moveTo(1320, 660, duration=0.5)
    pyautogui.click()
    pyautogui.moveTo(1320, 700, duration=0.5)
    time.sleep(30)


def fill_file(filename):
    pyautogui.moveTo(635, 810, duration=0.5)
    pyautogui.click()

    pyautogui.hotkey("command", "a")
    pyautogui.press("backspace")

    dest_path = os.path.join(destination_folder, filename)
    with open(dest_path, "r", encoding="utf-8") as file:
        content = file.read()
        data = f'"""\n{content}\n"""\nFor {filename}, I want all 10 rows in jsonl format and you must follow the prompt instructions'
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


def append_data(filename):
    y_cors = [263, 273, 283, 293, 303, 313,323,333,343,353,363, 373, 383, 393, 403, 413, 423, 433, 453, 463, 473]
    clipboard_data = ""
    num_rows = 0

    for y_cor in y_cors:
        copy(y_cor)
        clipboard_data = pyperclip.paste()
        clipboard_data = "\n".join(
            [line for line in clipboard_data.split("\n") if line.strip()]
        )
        clipboard_data += "\n"
        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)
        if num_rows == 10:
            break

    if num_rows != 10 or is_jsonl(lines) is False:
        clipboard_data = f"Error: {filename}, {num_rows}lines\n"

    with open("data/squad/translated.jsonl", "a", encoding="utf-8") as f:
        f.write(clipboard_data)


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
start = 2473
files = os.listdir(source_folder)
files = sorted(files, key=extract_number)[start:last]
is_first = True
count = 0
for filename in files:
    source_path = os.path.join(source_folder, filename)

    delete_temp_files()
    copy_file(filename)
    #upload_file(is_first, filename)
    if count == 0:
        fill_first(is_first)
    fill_file(filename)
    append_data(filename)

    pyautogui.moveTo(900, 850, duration=0.5)
    pyautogui.click()

    is_first = False
    count += 1
    if count >= 30:
        count = 0
        time.sleep(300)
