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


def upload_file(is_first, filename):
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


def append_data(filename):
    y_cors = [363, 373, 383, 393, 403, 413, 423, 433, 453, 463, 473]
    clipboard_data = ""
    num_rows = 0

    for y_cor in y_cors:
        copy(y_cor)
        clipboard_data = pyperclip.paste()
        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)
        if num_rows == 10:
            break

    if num_rows != 10:
        clipboard_data = f"Error: {filename}, {num_rows}lines\n"

    with open("data/squad/translated.jsonl", "a", encoding="utf-8") as f:
        f.write(clipboard_data)


def delete_temp_files():
    for filename in os.listdir(destination_folder):
        file_path = os.path.join(destination_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")


def copy_file():
    if os.path.isfile(source_path):
        dest_path = os.path.join(destination_folder, filename)
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")


def extract_number(filename):
    match = re.search(r"_(\d+)\.json$", filename)
    return int(match.group(1)) if match else -1


source_folder = "data/squad/processed/answers_chunks"
destination_folder = "temp/"


files = os.listdir(source_folder)
files = sorted(files, key=extract_number)[1973:]
is_first = True
for filename in files:
    source_path = os.path.join(source_folder, filename)

    delete_temp_files()
    copy_file()
    upload_file(is_first, filename)
    append_data(filename)

    pyautogui.moveTo(900, 850, duration=0.5)
    pyautogui.click()

    is_first = False
