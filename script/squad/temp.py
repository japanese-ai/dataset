import pyautogui
import pyperclip


pyautogui.moveTo(650, 610, duration=0.5)
pyautogui.click()

pyautogui.hotkey("command", "a")
pyautogui.press("backspace")

pyperclip.copy(
        "You must follow the prompt instructions and need to provide in jsonl format for the following questions"
)
pyautogui.hotkey("command", "v")

pyautogui.moveTo(1320, 660, duration=0.5)
