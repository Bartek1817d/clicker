from pynput import keyboard
from pynput import mouse
from time import sleep
from pynput.keyboard import Key
from threading import Thread

START_KEY = Key.ctrl_r
STOP_KEY = Key.esc

started = False
play_thread: Thread = None

keyboard_controller = keyboard.Controller()
mouse_controller = mouse.Controller()


def play():
    with open('keys.txt', 'r') as file:
        commands = [Command.create(line.split()) for line in file]

    while True:
        for command in commands:
            if not started:
                return
            sleep(1)
            command.execute()

def on_release(key):

    global started, play_thread

    if key == STOP_KEY:
        started = False
        return False

    if not started and key == START_KEY:
        started = True
        play_thread = Thread(target=play)
        play_thread.start()
        return

keyboard_listener = keyboard.Listener(on_release=on_release)

class Command:

    def execute(self):
        None

    @staticmethod
    def create(tokens: list):
        return MouseCommand(tokens[1:]) if tokens[0] == 'mouse' else KeyboardCommand(tokens[1:])


class MouseCommand(Command):
    controller = mouse_controller

    def __init__(self, tokens: list):
        self.x = int(tokens[0])
        self.y = int(tokens[1])
        self.double = len(tokens) > 2

    def execute(self):
        self.controller.position = (self.x, self.y)
        self.controller.click(mouse.Button.left, 2 if self.double else 1)


class KeyboardCommand(Command):
    controller = keyboard_controller

    def __init__(self, tokens: list):
        self.keys = [KeyboardCommand.parse_key(token) for token in tokens]

    def execute(self):
        for key in self.keys:
            self.controller.press(key)
        for key in reversed(self.keys):
            self.controller.release(key)

    @staticmethod
    def parse_key(token: str):
        if len(token) == 1:
            return keyboard.KeyCode.from_char(token)
        else:
            return keyboard.Key[token]

keyboard_listener.start()
keyboard_listener.join()
if play_thread:
    play_thread.join()
