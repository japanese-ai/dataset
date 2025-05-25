import json
import os
import re
import time
from abc import ABC, abstractmethod

import pyautogui
import pyperclip


class ChatGptUI(ABC):
    def __init__(self):
        self.folder_path = ""
        self.destination_file = ""
        self.new_chat_y_cor = 180
        self.new_chat_target_y_cor = 360
        self.message_x_cor = 470
        self.message_y_cor = 840
        self.message_put_x_cor = 1040
        self.message_put_y_cor = 880
        self.message_wait_x_cor = 1100
        self.message_wait_y_cor = 680
        self.wait_time = 120
        self.copy_x_cor = 950
        self.close_voice_x_cor = 660
        self.close_voice_y_cor = 890
        self.get_data_y_cors = []
        self.example_data = []

    def copy(self, filename, y_cor):
        pyperclip.copy(f"Error: {filename}\n")
        pyautogui.moveTo(self.copy_x_cor, y_cor, duration=0.5)
        pyautogui.click()
        pyautogui.click()

    def make_new_chat(self, is_first):
        pyautogui.moveTo(180, self.new_chat_y_cor, duration=0.5)
        if is_first:
            pyautogui.click()
        pyautogui.click()
        time.sleep(10)

        pyautogui.moveTo(180, self.new_chat_target_y_cor, duration=0.5)
        pyautogui.click()
        time.sleep(30)

    @abstractmethod
    def get_message(self, content, filename, index, num_rows):
        pass

    def fill_file(self, filename, index=0):
        pyautogui.moveTo(self.message_x_cor, self.message_y_cor, duration=0.5)
        pyautogui.click()

        pyautogui.hotkey("command", "a")
        pyautogui.press("backspace")

        file_path = os.path.join(self.folder_path, filename)
        num_rows = 10 if index == 0 else 5
        with open(file_path, "r", encoding="utf-8") as file:
            content = json.load(file)
            if index == 1:
                content = content[:5]
            elif index == 2:
                content = content[5:]

            data = self.get_message(content, filename, index, num_rows)
            pyperclip.copy(data)
            pyautogui.hotkey("command", "v")

        pyautogui.moveTo(self.message_put_x_cor, self.message_put_y_cor, duration=0.5)
        pyautogui.click()
        pyautogui.moveTo(self.message_wait_x_cor, self.message_wait_y_cor, duration=0.5)
        time.sleep(self.wait_time)

    def replace_with_fallback(self, data):
        patterns = [(r"\n},\n{", "\n}\n\n{"), (r"\n}\n{", "\n}\n\n{")]
        for pattern, replacement in patterns:
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                data = re.sub(pattern, replacement, data, flags=re.MULTILINE)
                break

        return data

    @abstractmethod
    def is_valid_format(self, obj):
        pass

    def is_jsonl(self, lines):
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if not self.is_valid_format(obj):
                    print(f"Invalid format in line {i}: {line}")
                    return False
            except json.JSONDecodeError:
                return False
        return True

    def get_clipboard_data(self, clipboard_data, check_rows):
        clipboard_data = clipboard_data.replace("</p>\n<p>", "</p><p>")
        clipboard_data = clipboard_data.replace("</li>\n  <li>", "</li><li>")
        clipboard_data = clipboard_data.replace("</li>\n<li>", "</li><li>")
        clipboard_data = clipboard_data.replace("\n<ul>\n  ", "<ul>")
        clipboard_data = clipboard_data.replace("\n</ul>\n", "</ul>")

        temp_lines = clipboard_data.strip().splitlines()

        if len(temp_lines) > 20:
            clipboard_data = self.replace_with_fallback(clipboard_data)
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
            clipboard_data = [
                (line.replace("}]}},", "}]}}")) for line in clipboard_data
            ]

        try:
            clipboard_data = [json.loads(obj) for obj in clipboard_data]
            clipboard_data = [json.dumps(obj, ensure_ascii=False) for obj in clipboard_data]
            clipboard_data = "\n".join(clipboard_data)
            clipboard_data += "\n"
        except:
            return False, 0, None, None

        if any(item in clipboard_data for item in self.example_data):
            return True, 0, None, None

        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)

        if num_rows == check_rows:
            return True, num_rows, clipboard_data, lines

        return False, 0, None, None

    def append_data(self, filename, index=0):
        pyautogui.scroll(-100)

        clipboard_data = ""
        num_rows = 0
        lines = []
        check_rows = 10 if index == 0 else 5
        for y_cor in self.get_data_y_cors:
            self.copy(filename, y_cor)
            clipboard_data = pyperclip.paste()
            got_data, num_rows, clipboard_data, lines = self.get_clipboard_data(
                clipboard_data, check_rows
            )

            if got_data:
                break

        is_appended = True
        if num_rows != check_rows or self.is_jsonl(lines) is False:
            clipboard_data = f"Error: {filename}, {num_rows}lines (index: {index})\n"
            is_appended = False

        with open(self.destination_file, "a", encoding="utf-8") as f:
            f.write(clipboard_data)

        return is_appended

    def check_clipboard_data(self, clipboard_data, check_rows):
        _, num_rows, clipboard_data, lines = self.get_clipboard_data(
            clipboard_data, check_rows
        )

        if num_rows == check_rows and self.is_jsonl(lines) is True:
            return True, clipboard_data

        return False, None

    def extract_number(self, filename):
        match = re.search(r"_(\d+)\.json$", filename)
        return int(match.group(1)) if match else -1

    def start_get_data(
        self, start, end=None, start_from_new_chat=True, start_from_half=False,
    ):
        files = os.listdir(self.folder_path)

        files = sorted(files, key=self.extract_number)
        files = files[start:end] if end is not None else files[start:]

        is_first = True
        count = 0 if start_from_new_chat else 1
        error_count = 0

        for filename in files:
            if count == 0:
                self.make_new_chat(is_first)

            for index in [2] if start_from_half else [1, 2]:
                self.fill_file(filename, index)
                is_appended = self.append_data(filename, index)
                if is_appended is True:
                    error_count = 0
                else:
                    error_count += 1

            pyautogui.moveTo(
                self.close_voice_x_cor, self.close_voice_y_cor, duration=0.5
            )
            pyautogui.click()

            is_first = False
            start_from_half = False

            count += 1
            if count > 15:
                count = 0
                time.sleep(300)

            if error_count >= 5:
                break
