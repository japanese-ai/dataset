import json
import re
import time
from abc import ABC, abstractmethod
from collections import OrderedDict

import pyautogui
import pyperclip


class ChatGptUI(ABC):
    def __init__(self):
        self.have_no = False
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
        self.current_start_no = 0

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

    def get_append_data(self, content, batch_str):
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
        line_break = "\n" * len(content)
        if num_rows == len(content):
            valid, message = self.is_jsonl(lines)
            if not valid:
                clipboard_data = f"Error: {batch_str} - {message}{line_break}"
                is_appended = False
        else:
            clipboard_data = (
                f"Error: {batch_str} - Only have {num_rows} rows{line_break}"
            )
            is_appended = False

        return is_appended, clipboard_data

    def append_data(self, content, batch_str):
        is_appended, clipboard_data = self.get_append_data(content, batch_str)

        with open(self.destination_file, "a", encoding="utf-8") as f:
            f.write(clipboard_data)

        return is_appended

    def append_error_data(self, error_data, content, batch_str):
        is_appended, clipboard_data = self.get_append_data(content, batch_str)

        error_blank_len = len(content) - 1
        data_list = []
        with open(self.destination_file, "r", encoding="utf-8") as f:
            is_found = False
            for line in f:
                if is_found and line.strip() == "" and error_blank_len > 0:
                    error_blank_len -= 1
                    continue

                if line == error_data["line"] and is_found is False:
                    data_list.append(clipboard_data)
                    is_found = True
                else:
                    data_list.append(line)

        with open(self.destination_file, "w", encoding="utf-8") as f:
            f.write("".join(data_list))

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
            self.current_start_no = start + i + 1
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

    def get_error_data(self, start_from_new_chat=True):
        is_first = True
        count = 0 if start_from_new_chat else 1
        error_count = 0

        with open(self.input_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        error_data_list = []
        with open(self.destination_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("Error: "):
                    remove_line = line.strip().replace("Error: ", "")
                    data = remove_line.split(" - ")
                    error_data_list.append(
                        {"line": line, "start": int(data[0]), "end": int(data[1])}
                    )

        for error_data in error_data_list:
            if count == 0:
                self.make_new_chat(is_first)

            content = data_list[(error_data["start"] - 1) : error_data["end"]]
            batch_str = f"{error_data['start']} - {error_data['end']}"
            self.current_start_no = error_data["start"]

            self.fill_content(content, batch_str)
            is_appended = self.append_error_data(error_data, content, batch_str)
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

    def add_no_to_output(self):
        fixed_data = []

        with open(self.destination_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue

                data = json.loads(line)

                new_obj = OrderedDict()
                new_obj["no"] = idx + 1
                for k, v in data.items():
                    new_obj[k] = v

                fixed_data.append(new_obj)

        with open(self.destination_file, "w", encoding="utf-8") as f:
            for item in fixed_data:
                json.dump(item, f, ensure_ascii=False)
                f.write("\n")

    def extract_invalid_data_from_output(self, invalid_file):
        with open(self.destination_file, "r", encoding="utf-8") as f:
            data_list = [json.loads(line) for line in f]

        error_list = []
        for data in data_list:
            valid, message = self.is_valid_format(data)
            if not valid:
                error_list.append({"no": data.get("no"), "message": message})

        with open(invalid_file, "w", encoding="utf-8") as f:
            for eror in error_list:
                json.dump(eror, f, ensure_ascii=False)
                f.write("\n")

        return error_list

    def append_invalid_fixed_data(self, content, batch_str, invalid_file, fix_file):
        is_appended, clipboard_data = self.get_append_data(content, batch_str)

        if not is_appended:
            return False

        # Append fixed data
        with open(fix_file, "a", encoding="utf-8") as f:
            f.write(clipboard_data)

        fixed_no_set = {obj.get("no") for obj in content}

        # Read invalid entries and keep only those not fixed
        remaining_invalids = []
        with open(invalid_file, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                if obj.get("no") not in fixed_no_set:
                    remaining_invalids.append(obj)

        # Overwrite invalid_file with remaining entries
        with open(invalid_file, "w", encoding="utf-8") as f:
            for obj in remaining_invalids:
                json.dump(obj, f, ensure_ascii=False)
                f.write("\n")

        return True

    def fix_invalid_data(self, invalid_file, fix_file, start_from_new_chat=True):
        # get data from invalid_file
        with open(invalid_file, "r", encoding="utf-8") as f:
            invalid_list = [json.loads(line) for line in f]
            invalid_no_list = [item["no"] for item in invalid_list]

        # get data from destination_file
        error_data_list = []
        with open(self.destination_file, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                if obj.get("no") in invalid_no_list:
                    error_data_list.append(obj)

        # get data fro ui
        is_first = True
        count = 0 if start_from_new_chat else 1
        error_count = 0

        for i in range(0, len(error_data_list), self.batch_size):
            if count == 0:
                self.make_new_chat(is_first)

            content = error_data_list[i : i + self.batch_size]
            batch_str = ", ".join([str(obj.get("no")) for obj in content])
            self.current_start_no = content[-1].get("no")
            self.fill_content(content, batch_str)
            is_appended = self.append_invalid_fixed_data(
                content, batch_str, invalid_file, fix_file
            )
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

    def merge_fixed_data(self, fixed_file):
        merged = {}

        with open(self.destination_file, "r", encoding="utf-8") as f1:
            for line in f1:
                obj = json.loads(line)
                merged[obj["no"]] = obj

        with open(fixed_file, "r", encoding="utf-8") as f2:
            for line in f2:
                obj = json.loads(line)
                no = obj["no"]
                if no in merged:
                    new_obj = {}
                    for key in merged[no]:
                        new_obj[key] = obj.get(key, merged[no][key])
                    merged[no] = new_obj

        # Write merged results
        with open(self.destination_file, "w", encoding="utf-8") as out:
            for obj in merged.values():
                json.dump(obj, out, ensure_ascii=False)
                out.write("\n")
