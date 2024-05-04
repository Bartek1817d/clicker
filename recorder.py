from pynput import keyboard, mouse
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button
from time import time

file = open("keys.txt", "w")

START_KEY = Key.ctrl_r
STOP_KEY = Key.esc
DOUBLE_CLICK_TIME = 0.3

pressed_keys = []
started = False
click_time = 0


def on_press(key):
    if not started or key == STOP_KEY:
        return

    if not pressed_keys:
        file.write('key')

    if isinstance(key, KeyCode):
        file.write(' ' + key.char)
        pressed_keys.append(key.char)
    elif isinstance(key, Key):
        file.write(' ' + key.name)
        pressed_keys.append(key.name)


def on_release(key):
    global started

    if key == STOP_KEY:
        mouse_listener.stop()
        return False

    if not started:
        if key == START_KEY:
            started = True
        return

    if isinstance(key, KeyCode):
        pressed_keys.remove(key.char)
    elif isinstance(key, Key):
        pressed_keys.remove(key.name)

    if not pressed_keys:
        file.write('\n')


def on_click(x, y, button, pressed):
    global click_time

    if not started:
        return

    if pressed and button == Button.left:
        t = time()
        if t - click_time < DOUBLE_CLICK_TIME:
            file.seek(file.tell() - 1)
            file.write(' double\n')
        else:
            file.write('mouse {} {}\n'.format(x, y))
        click_time = t


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()
file.close()
