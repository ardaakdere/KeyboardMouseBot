import pyautogui
import json
from time import sleep, time
import pyperclip

events = None

SCROLL_SENSITIVE = 110

CHANGE_LETTERS = {
    'alt_l': 'altleft',
    'alt_r': 'altright',
    'alt_gr': 'altright',
    'ctrl_l': 'ctrlleft',
    'ctrl_r': 'ctrlright',
    'shift_l': 'shiftleft',
    'shift_r': 'shiftright',
    'page_down': 'pagedown',
    'page_up': 'pageup',
    'caps_lock': 'capslock',
    'media_volume_down': 'volumedown',
    'media_volume_up': 'volumeup',
    'print_screen': 'printscreen',
    'num_lock': 'numlock',
    'scroll_lock': 'scrolllock'
}

UTF_CHARACTERS = ['ç','ı', 'ö', 'ş', 'ğ', 'ü', '@', 'İ']

def ConvertToProperKeys(key):

    properKey = key.replace('Key.', '')

    if properKey in CHANGE_LETTERS.keys():
        return CHANGE_LETTERS[properKey]
    elif properKey in UTF_CHARACTERS:
        pyperclip.copy(properKey)
        pyautogui.hotkey('ctrl', 'v')
        return ''

    return properKey


def load_json():
    global events
    with open('events.json', 'r') as event:
        events = json.load(event)

def play():
    global SCROLL_SENSITIVE
    for x, y in enumerate(events[1:]):
        p = y['time'] -0.1# hızlandırılmak istenirse girilebilir bi parametre 
        sleep(p if p > 0 else 0)
        if y['action'] == 0:
            pyautogui.keyDown(ConvertToProperKeys(y['key']))
        elif y['action'] == 1:
            pyautogui.keyUp(ConvertToProperKeys(y['key']))
        elif y['action'] == 2:
            pyautogui.moveTo(x = y['coordinate'][0], y = y['coordinate'][1])
        elif y['action'] == 3:
            pyautogui.click(x = y['coordinate'][0], y = y['coordinate'][1])
        elif y['action'] == 4:
            pyautogui.scroll(clicks=(SCROLL_SENSITIVE if y['direction'] == 'up' else -SCROLL_SENSITIVE), x = y['coordinate'][0], y = y['coordinate'][1])

def run():
    load_json()
    print('Starting within 5 seconds')
    sleep(5)
    play()
    pyautogui.keyUp('esc')
if __name__ == '__main__':
    run()