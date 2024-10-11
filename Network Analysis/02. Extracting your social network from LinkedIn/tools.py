import re
import time
import random
import pyautogui


def remove_polish_chars(text: str) -> str:
    mapping = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ż': 'z', 'ź': 'z'}
    return ''.join(mapping.get(char, char) for char in text)


def type_polish_text(text: str, interval: float):
    special_chars = {
        'ą': ('altgr', 'a'),
        'ć': ('altgr', 'c'),
        'ę': ('altgr', 'e'),
        'ł': ('altgr', 'l'),
        'ń': ('altgr', 'n'),
        'ó': ('altgr', 'o'),
        'ś': ('altgr', 's'),
        'ż': ('altgr', 'z'),
        'ź': ('altgr', 'x')
    }
    for char in text.lower():
        if char in special_chars:
            shortcut(*special_chars[char])
        else: pyautogui.press(char)
        time.sleep(random.random() * interval)


def shortcut(hold: str, press: str):
    pyautogui.keyDown(hold)
    pyautogui.press(press)
    pyautogui.keyUp(hold)


def run_instructions(instructions: list[str]):
    for inst in instructions:
        if m := re.match('click_([0-9]+)_([0-9]+)', inst):
            # print('move to', m.group(1), m.group(2), 'and click')
            pyautogui.moveTo(int(m.group(1)), int(m.group(2)), duration=random.random())
            pyautogui.click()
        elif m := re.match('type_(.+)', inst):
            # print('type', m.group(1))
            type_polish_text(m.group(1), interval=0.1)
        elif m := re.match('press_(.+)', inst):
            # print('press', m.group(1))
            pyautogui.press(m.group(1))
        elif m := re.match('shortcut_(.+)_(.+)', inst):
            # print('shortcut', m.group(1), m.group(2))
            shortcut(m.group(1), m.group(2))
        else: print(f'!!! Unknown instruction {inst} !!!')
        time.sleep(0.5 + random.random())