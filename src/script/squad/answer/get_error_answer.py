import json
import time

import pyautogui
import pyperclip

from script.squad.plausible_answer import PlausibleAnswer

plausible = PlausibleAnswer()
plausible.have_no = True

no_list = []


def append_data(content, batch_str):
    pyautogui.scroll(-100)
    y_cors = list(range(177, 588, 10))

    clipboard_data = ""
    num_rows = 0
    lines = []
    for y_cor in y_cors:
        plausible.copy(batch_str, y_cor)
        clipboard_data = pyperclip.paste()
        got_data, num_rows, clipboard_data, lines = plausible.get_clipboard_data(
            clipboard_data, len(content)
        )

        if got_data:
            break

    is_appended = True
    if num_rows == len(content):
        valid, message = plausible.is_jsonl(lines)
        if valid:
            temp_lines = clipboard_data.strip().splitlines()
            temp_lines = [json.loads(obj) for obj in temp_lines]
            valid_no_list = [item["no"] for item in temp_lines]

            exist = all(item in no_list for item in valid_no_list)

            if not exist:
                is_appended = False
                clipboard_data = (
                    f"Error: {batch_str} - all no are not included \n\n\n\n\n"
                )

        else:
            clipboard_data = f"Error: {batch_str} - {message}\n\n\n\n\n"
            is_appended = False
    else:
        clipboard_data = f"Error: {batch_str} - Only have {num_rows} rows\n\n\n\n\n"
        is_appended = False

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(clipboard_data)

    return is_appended


input_file = "data/squad/plausible_translated_answer.jsonl"
output_file = "data/squad/plausible_translated_answer_fixed.jsonl"


# read file
with open(input_file, "r", encoding="utf-8") as f:
    data_list = [json.loads(line) for line in f]

start = 2215
count = 1
error_count = 0
data_list = data_list[start:]
batch_size = 5
is_first = True

plausible.wait_time = 180


for i in range(0, len(data_list), batch_size):
    data = data_list[i : i + batch_size]

    no_list = [item["no"] for item in data]
    str_no = ", ".join(map(str, no_list))
    str_no = f"[{str_no}]"

    if no_list[-1] >= 21740:
        plausible.have_graph_data = True
    else:
        plausible.have_graph_data = False

    if count == 0:
        plausible.make_new_chat(is_first)

    plausible.fill_content(data, str_no)

    is_appended = append_data(data, str_no)
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
