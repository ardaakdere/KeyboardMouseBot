from pynput import mouse, keyboard
from time import time, sleep
import json

mouse_listener = None
start_time = None
last_coordinate = [0,0]
# MAUS HASSASİYETİ -- (HASSASİYET ARTTIKÇA DAHA YAVAŞ ÇALIŞIR).
THRESHOLD = 200
upToNow = 0
events = []

def save_json():
    with open('events.json', 'w') as event:
        json.dump(events, event,indent=4)

# For Keyboard --
# from pynput doc.
def on_press(key):
    #current_time = time()
    try:
        save_event(current_time=round(time(),2), action=0, key = key.char)
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        save_event(current_time=round(time(),2), action=0, key = str(key))
        print('special key {0} pressed'.format(
            key))

# from pynput doc.
def on_release(key):
    try:
        print('{0} released'.format(
        key))
        if key == keyboard.Key.esc:
            print(time()-start_time)
            # returning False stops the keyboard listener, using stop function to stop mouse listener
            mouse_listener.stop()
            save_json()
            print('Mouse and Keyboard listener has stopped')
            return False
        save_event(current_time=round(time(),2), action=1, key = key.char)
    except:
        save_event(current_time=round(time(),2), action=1, key = str(key))
# For Keyboard --

# For Mouse --
def on_move(x, y):
    save_event(current_time=round(time(),2), action=2, coordinate=[x,y])
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    if pressed:
        save_event(current_time=round(time(),2), action=3, coordinate=[x,y])
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))

def on_scroll(x, y, dx, dy):
    save_event(current_time=round(time(),2), action=4, coordinate=[x,y], direction = ('down' if dy < 0 else 'up'))
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))
# For Mouse --

class ActionTypes():
    KEYPRESS = 0
    KEYRELEASE = 1
    MOUSEMOVE = 2
    MOUSECLICK = 3
    MOUSESCROLL = 4

# 0 --> keypress
# 1 --> keyrelease
# 2 --> mousemove
# 3 --> mouseclick
# 4 --> mousescroll
def save_event(current_time, action, key='', coordinate=[], direction = 'up'):
    global upToNow
    elapsed_time = current_time-start_time
    theduration = round(elapsed_time - upToNow, 2)
    if action == ActionTypes.KEYPRESS:
        info = {
            'time': theduration,
            'action': ActionTypes.KEYPRESS,
            'key': key
        }
    elif action == ActionTypes.KEYRELEASE:
        info = {
            'time': theduration,
            'action': ActionTypes.KEYRELEASE,
            'key': key
        }
    elif action == ActionTypes.MOUSEMOVE:
        global last_coordinate
        if abs(coordinate[0] - last_coordinate[0]) > THRESHOLD or abs(coordinate[1] - last_coordinate[1]) > THRESHOLD:
            info = {
                'time': 0,
                'action': ActionTypes.MOUSEMOVE,
                'coordinate': coordinate
            }
            last_coordinate = coordinate
            # mouse move için ayrı bir append yazdık çünkü her farklı koordinatı kaydetmek yerine
            # sadece bir öncekiyle 200 piksellik fark olan hareketleri kaydedeceğiz ve kaydettikten sonra
            # koşul sonrası append 'e de düşmemesi için return ediyorum.
            events.append(info)
        return
    elif action == ActionTypes.MOUSECLICK:
        info = {
            'time': theduration,
            'action': ActionTypes.MOUSECLICK,
            'coordinate': coordinate
        }
    elif action == ActionTypes.MOUSESCROLL:
        info = {
            'time': theduration,
            'action': ActionTypes.MOUSESCROLL,
            'coordinate': coordinate,
            'direction': direction
        }
    upToNow = elapsed_time
    events.append(info)


def settingUpMouseSensitive():
    global THRESHOLD
    print('Mouse Sensitive is 200. If you want, you can set different value:')
    while True:
        print('Do you want to change?')
        response = input('Y/N').lower()
        if response == 'y':
            try:
                sensitive = int(input('Enter the sensitive (0-300):'))
                if 0 <= sensitive <= 300:
                    THRESHOLD = sensitive
                    print(f'Sensitive has changed. ({sensitive})')
                    break
                else:
                    print('Please enter proper value.')
            except:
                print('Please enter proper value.')
        elif response == 'n':
            print(f'Sensitive is {THRESHOLD}')
            break

def run():
    global start_time
    settingUpMouseSensitive()
    input('Type anything and enter to start recording')
    for x in range(4, -1, -1):
        print(x+1)
        sleep(1)
    print('Recording...')
    start_time = round(time(),2)
    print(start_time)

    events.append({'time': 0, 'action': 'Recording Started'})
    global mouse_listener

    # Collect events until released
    keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
    
    # Collect events until released
    mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()

    print(events)

if __name__ == '__main__':
    run()