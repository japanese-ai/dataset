import json
import re
import time
from abc import ABC, abstractmethod

import pyautogui
import pyperclip


class ChatGptUI(ABC):
    def __init__(self):
        self.input_file = ""
        self.destination_file = ""
        self.batch_size = 5
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

    def copy(self, batch_str, y_cor):
        pyperclip.copy(f"Error: {batch_str}")
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
    def get_message(self, content, num_rows):
        pass

    def fill_content(self, content, batch_str):
        pyautogui.moveTo(self.message_x_cor, self.message_y_cor, duration=0.5)
        pyautogui.click()

        pyautogui.hotkey("command", "a")
        pyautogui.press("backspace")

        data = self.get_message(content, batch_str, len(content))
        pyperclip.copy(data)
        pyautogui.hotkey("command", "v")

        pyautogui.moveTo(self.message_put_x_cor, self.message_put_y_cor, duration=0.5)
        pyautogui.click()
        pyautogui.moveTo(self.message_wait_x_cor, self.message_wait_y_cor, duration=0.5)
        time.sleep(self.wait_time)

    def replace_with_fallback(self, data):
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
                valid, message = self.is_valid_format(obj)
                if not valid:
                    return False, f"Line {i}: {message}"
            except json.JSONDecodeError as e:
                return False, f"Line {i}: {str(e)}"
        return True, ""

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
            clipboard_data = [
                json.dumps(obj, ensure_ascii=False) for obj in clipboard_data
            ]
            clipboard_data = "\n".join(clipboard_data)
            clipboard_data += "\n"
        except Exception:
            return False, 0, None, None

        if any(item in clipboard_data for item in self.example_data):
            return True, 0, None, None

        lines = clipboard_data.strip().splitlines()
        num_rows = len(lines)

        if num_rows == check_rows:
            return True, num_rows, clipboard_data, lines

        return False, 0, None, None

    def append_data(self, content, batch_str):
        pyautogui.scroll(-100)

        clipboard_data = ""
        num_rows = 0
        lines = []
        for y_cor in self.get_data_y_cors:
            self.copy(batch_str, y_cor)
            clipboard_data = pyperclip.paste()
            got_data, num_rows, clipboard_data, lines = self.get_clipboard_data(
                clipboard_data, len(content)
            )

            if got_data:
                break

        is_appended = True
        if num_rows == len(content):
            valid, message = self.is_jsonl(lines)
            if not valid:
                clipboard_data = f"Error: {batch_str} - {message}\n\n\n\n\n"
                is_appended = False
        else:
            clipboard_data = f"Error: {batch_str} - Only have {num_rows} rows\n\n\n\n\n"
            is_appended = False

        with open(self.destination_file, "a", encoding="utf-8") as f:
            f.write(clipboard_data)

        return is_appended

    def check_clipboard_data(self, clipboard_data, check_rows):
        _, num_rows, clipboard_data, lines = self.get_clipboard_data(
            clipboard_data, check_rows
        )

        if num_rows == check_rows:
            valid, message = self.is_jsonl(lines)
        else:
            valid = False
            message = f"Only have {num_rows} rows"

        return valid, clipboard_data, message

    def start_get_data(
        self,
        start,
        end=None,
        start_from_new_chat=True,
    ):
        is_first = True
        count = 0 if start_from_new_chat else 1
        error_count = 0

        with open(self.input_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        data_list = data_list[start:] if end is None else data_list[start:end]
        for i in range(0, len(data_list), self.batch_size):
            if count == 0:
                self.make_new_chat(is_first)

            content = data_list[i : i + self.batch_size]
            batch_str = f"{start + i + 1} - {start + i + self.batch_size}"
            self.fill_content(content, batch_str)
            is_appended = self.append_data(content, batch_str)
            if is_appended is True:
                error_count = 0
            else:
                error_count += 1

            pyautogui.moveTo(
                self.close_voice_x_cor, self.close_voice_y_cor, duration=0.5
            )
            pyautogui.click()

            is_first = False

            count += 1
            if count > 15:
                count = 0
                time.sleep(300)

            if error_count >= 5:
                break
