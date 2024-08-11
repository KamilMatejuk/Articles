import pyautogui
from pynput import keyboard


positions = []
descriptions = {
    'BROWSER_LINK': 'Position of the link in browser',
    'DROPDOWN': 'Position of connection dropdown',
    'SEARCH_FIELD': 'Position of search filed inside connection dropdown',
    'CHOOSE_FIRST_FOUND': 'Position of first candidate after searching',
    'SHOW_RESULTS': 'Position of button to show results after chooseing new connection',
    # 'MARGIN': 'Anyplace on page that won\'t click anythink and unfocus the search',
    'SAVE_WINDOW': 'Anyplace on the saving window that will focus it',
    'SAVE_WINDOW_BTN': 'POsition of button to save file',
}
outfile = 'coordinates.py'


def on_press(key):
    if key != keyboard.Key.space: return
    x, y = pyautogui.position()
    positions.append((x, y))
    print(x, y)
    return False


for desc in descriptions.values():
    print(f'Move mouse and press space to choose: {desc}')
    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        listener.join()

with open(outfile, 'w+') as f:
    for name, (x, y) in zip(descriptions.keys(), positions):
        f.write(f'{name} = ({x}, {y})\n')

print(f'Saved coordinates to {outfile}')
