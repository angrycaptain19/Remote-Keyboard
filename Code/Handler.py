from http.server import BaseHTTPRequestHandler
from pynput import keyboard
from urllib.parse import unquote
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def update_html(cls):
    with open(resource_path('.\\templates\\js\\script.js'), 'rt') as file: data = file.read()

    data = data.replace(data[data.find('const ip =') : data.find('const ip =') + 39], f"const ip = 'http://{cls.IP}:8000/'; ")
    with open(resource_path('.\\templates\\js\\script.js'), 'wt') as file:
        file.write(data)
        # RHandler.file = data

controller = keyboard.Controller()
class RHandler(BaseHTTPRequestHandler):

    running = True
    wordout = 'CodeEscape_Exit'
    html = ''
    js = ''
    css = ''

    special = {
        'ctrl': keyboard.Key.ctrl,
        'alt': keyboard.Key.alt_gr,
        'shift': keyboard.Key.shift
    }

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

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', RHandler.IP)
        self.end_headers()

    def do_GET(self):
        self._set_response()

        if self.req_file(posible = ['/', '/HTML.html', ], variable = self.html, location = 'HTML.html'): pass

        elif self.req_file(posible = ['/css/style.css'], variable = self.css, location = 'css\\style.css'): pass

        elif self.req_file(posible = ['/js/script.js'], variable = self.js, location = 'js\\script.js'): pass

        elif "keyboard.Key" in self.path:
            pos = self.path.rfind('?')

            maybe_special = self.path[self.path.find('keyboard.Key') + 13 : pos]

            if maybe_special in self.special: self.special_key(pos = pos, maybe_special = maybe_special)

            else: self.repeat_key(pos = pos)

        else: self.just_text()

    def path_parser(self):
        return unquote(self.path[1:]).replace('favicon.ico', '')

    def log_message(self, format, *args):
        return

    def req_file(self, posible, variable, location):
        if self.path in posible:
            if not len(variable):
                with open(resource_path(f'.\\templates\\{location}'), 'rt') as file: variable = file.read()
            self.wfile.write(variable.encode('utf-8'))
            return True
        return False

    def special_key(self, pos, maybe_special):
        try: key_letter = keyboard.KeyCode(char=self.path[pos + 1].lower())
        except IndexError: key_letter = False

        key = self.special[maybe_special]

        controller.press(key)
        if key_letter: controller.press(key_letter)
        controller.release(key)
        if key_letter: controller.release(key_letter)


    def repeat_key(self, pos):
        try: tot = int(self.path[pos + 1:])
        except ValueError: tot = 1

        key_name = self.path[self.path.find('keyboard.Key') + 13 : pos]

        for i in range(tot): controller.tap(self.repeat[key_name])

    def just_text(self):
        word = self.path_parser()

        if word == self.wordout: RHandler.running = False

        else: controller.type(word)

