# Networking
from http.server import BaseHTTPRequestHandler

# Keyboard
from pynput import keyboard

# URL parsing
from urllib.parse import unquote

# PyInstaller patches
import sys
import os

# Keyword for special/repeat keys.
KEYWORD_KEY = 'keyboard.Key.'

# Workaround for PyInstaller dependencies.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Updates script.js with current IP for permissions and requests.
def update_ip(cls):
    with open(resource_path('.\\templates\\js\\script.js'), 'rt') as file: data = file.read()

    data = data.replace(data[data.find('const ip =') : data.find('const ip =') + 39], f"const ip = 'http://{cls.IP}:8000/'; ")
    with open(resource_path('.\\templates\\js\\script.js'), 'wt') as file: file.write(data)

# Keyboard controller for key-pressing.
controller = keyboard.Controller()

# Class RHandler for server.
class RHandler(BaseHTTPRequestHandler):

    running = True

    # Exit keyword
    wordout = 'CodeEscape_Exit'

    # Project files
    files = {
        'html' : '',
        'js' : '',
        'css' : ''
    }

    # Special keys
    special = {
        'ctrl': keyboard.Key.ctrl,
        'alt': keyboard.Key.alt_gr,
        'shift': keyboard.Key.shift
    }

    # Repeat keys
    repeat = {
        'enter' : keyboard.Key.enter,
        'up' : keyboard.Key.up,
        'down' : keyboard.Key.down,
        'left' : keyboard.Key.left,
        'right' : keyboard.Key.right,
        'backspace' : keyboard.Key.backspace,
        'space' : keyboard.Key.space,
        'delete' : keyboard.Key.delete,
        'esc' : keyboard.Key.esc
    }

    # Sends response to client
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', RHandler.IP)
        self.end_headers()

    # GET handling
    def do_GET(self):
        self._set_response()

        # Checks request for HTML
        if self.req_file(posible = ['/', '/HTML.html', ], variable = 'html', location = 'HTML.html'): pass

        # Checks requets for CSS
        elif self.req_file(posible = ['/css/style.css'], variable = 'css', location = 'css\\style.css'): pass

        # Checks requst for JS
        elif self.req_file(posible = ['/js/script.js'], variable = 'js', location = 'js\\script.js'): pass

        # Checks special/repeat keys
        elif KEYWORD_KEY in self.path:
            pos = self.path.rfind('?')

            maybe_special = self.path[self.path.find(KEYWORD_KEY) + len(KEYWORD_KEY) : pos]

            # Special key handling
            if maybe_special in self.special: self.special_key(pos = pos, maybe_special = maybe_special)

            # Repeat key handling
            else: self.repeat_key(pos = pos)

        # Text input handling
        else: self.just_text()

    # Input parser from URL to usable info
    def path_parser(self):
        return unquote(self.path[1:]).replace('favicon.ico', '')

    # Prevents server from logging output
    def log_message(self, format, *args):
        return

    # Loads file and writes it to client
    def req_file(self, posible : [list[str], tuple[str]], variable : str, location : str):

        # Checks if path is one of the posibilities
        if self.path in posible:

            # Checks if file has already been loaded
            if not len(self.files[variable]):

                # Loads file in its key from self.files
                with open(resource_path(f'.\\templates\\{location}'), 'rt') as file: self.files[variable] = file.read()

            # Writes output to client
            self.wfile.write(self.files[variable].encode('utf-8'))
            return True

        return False

    # Special key handling
    def special_key(self, pos : int, maybe_special : str):

        # Checks if special key comes with extra letter
        try: key_letter = keyboard.KeyCode(char=self.path[pos + 1].lower())
        except IndexError: key_letter = False

        # Translates special key
        key = self.special[maybe_special]

        # Presses and releases (Hot)Key.
        controller.press(key)
        if key_letter: controller.press(key_letter)
        controller.release(key)
        if key_letter: controller.release(key_letter)

    # Repeat key handling
    def repeat_key(self, pos : int):

        # Input parser for repeat amount
        try: tot = int(self.path[pos + 1:])
        except ValueError or IndexError: tot = 1

        # Translates repeat key
        key_name = self.path[self.path.find(KEYWORD_KEY) + len(KEYWORD_KEY) : pos]

        # Taps key {tot} times
        for _ in range(tot): controller.tap(self.repeat[key_name])

    # Text input handling
    def just_text(self):

        # Input parser from path
        word = self.path_parser()

        # If word matches exit sequence, sets running flag to False
        if word == self.wordout: RHandler.running = False

        # If word doesn't match exit sequence, types word
        else: controller.type(word)

