from http.server import BaseHTTPRequestHandler
from pynput import keyboard
from urllib.parse import unquote


def update_html(cls):
    with open('./templates/Remote.html', 'rt') as file: data = file.read()

    data = data.replace(data[data.find('const ip =') : data.find('const ip =') + 39], f"const ip = 'http://{cls.IP}:8000/'; ")
    with open('./templates/Remote.html', 'wt') as file: file.write(data)

controller = keyboard.Controller()
class RHandler(BaseHTTPRequestHandler):

    running = True
    wordout = 'CodeEscape_Exit'

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', RHandler.IP)
        self.end_headers()

    def do_GET(self):
        self._set_response()

        if self.path in ['/', '/Remote.html']:
            with open('./templates/Remote.html', 'rt') as file: res = file.read()
            self.wfile.write(res.encode('utf-8'))

        elif "keyboard.Key" in self.path:
            pos = self.path.rfind('?')
            try: tot = int(self.path[pos + 1 : ])
            except ValueError: tot = 1
            for i in range(tot): exec(f"controller.tap({self.path[self.path.find('keyboard.Key') : pos]})")

        else:
            word = self.path_parser()
            if word == self.wordout: RHandler.running = False
            else: controller.type(word)

    def path_parser(self):

        return unquote(self.path[1:]).replace('favicon.ico', '')

        # res = self.decode()

    def log_message(self, format, *args):
        return

    # def decode(self):
    #     res = self.path[1:]
    #     replacers = {
    #         '%C3%A1': 'á',
    #         '%C3%A9': 'é',
    #         '%C3%AD': 'í',
    #         '%C3%B3': 'ó',
    #         '%C3%BA': 'ú',
    #         '%C3%81': 'Á',
    #         '%C3%89': 'É',
    #         '%C3%8D': 'Í',
    #         '%C3%93': 'Ó',
    #         '%C3%9A': 'Ú',
    #         '%C2%BF': '¿',
    #         '%C2%A1': '¡',
    #         '%C3%B1': 'ñ',
    #         '%7B'   : '{',
    #         '%7D'   : '}',
    #         '%22'   : '"',
    #         '%20'   : ' ',
    #         '%5E'   : '^',
    #         '%3C'   : '<',
    #         '%3E'   : '>',
    #         '%7C'   : '|',
    #     }
    #
    #     for wrong, right in replacers.items(): res = res.replace(wrong, right)
    #     return res