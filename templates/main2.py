from threading import Thread
from http.server import HTTPServer
from time import sleep
from socket import gethostname, gethostbyname
from http.server import BaseHTTPRequestHandler
from pynput import keyboard
from urllib.parse import unquote

data = ["""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Remote control for computer</title>
</head>
<body>
<center>
    <button id = "Exit" onclick = myFunc("Exit")>Exit</button>
<input type = "text" id = "words">
<button id = "Button" value = "Go" onclick=myFunc("Go")>Send </button><br>
    <button id = "Button4" value = "Esc" onclick = myFunc("esc")>Esc</button>
    <button id = "Button2" value = "Enter" onclick = myFunc("enter")>Enter</button>
<button id = "Button3" value = "Backspace" onclick = myFunc("backspace")>Back</button>
    <button id = "Button10" value = "Delete" onclick = myFunc("delete")>Supr</button><br>

    <button id = "Button5" value = "Up" onclick = myFunc("up")>Up</button><br>
<button id = "Button7" value = "Left" onclick = myFunc("left")>Left</button>
<button id = "Button6" value = "Down" onclick = myFunc("down")>Down</button>
<button id = "Button8" value = "Right" onclick = myFunc("right")>Right</button><br>
    <button id = "Button9" value = "Space" onclick = myFunc("space")>Space</button>

</center>


<script>

    const myFunc = keyword => {

        const ip = 'http://192.168.0.96:8000/';                                                   
        let sender = ip;
        let x = new XMLHttpRequest();
        x.onreadystatechange = ()=>{
            if (x.readyState === 4 && x.status === 200)
                document.getElementById("words").value = ''
        };
        if (keyword === "Exit") sender += "CodeEscape_Exit";
        else if (keyword === 'Go') sender += document.getElementById("words").value;
        else sender += "keyboard.Key." + keyword + "?" + document.getElementById("words").value;

        x.open("GET", sender, true);
        x.send( null );
    };


</script>
</body>
</html>
"""]

def update_html(cls):
    data[0] = data[0].replace(data[0][data[0].find('const ip =') : data[0].find('const ip =') + 39], f"const ip = 'http://{cls.IP}:8000/'; ")

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

        if self.path in ['/', '/Remote.html']: self.wfile.write(data[0].encode('utf-8'))

        elif "keyboard.Key" in self.path:
            pos = self.path.rfind('?')
            try: tot = int(self.path[pos + 1 : ])
            except ValueError: tot = 1
            for i in range(tot): exec(f"controller.tap({self.path[self.path.find('keyboard.Key') : pos]})")

        else:
            word = self.path_parser()
            if word == self.wordout: RHandler.running = False
            else: controller.type(word)

    def path_parser(self): return unquote(self.path[1:]).replace('favicon.ico', '')

    def log_message(self, format, *args):
        return

myIP = gethostbyname(gethostname())
RHandler.IP = myIP
update_html(RHandler)

def create_server(port = 8000) -> tuple[Thread, HTTPServer]:
    server = HTTPServer(server_address=('', port), RequestHandlerClass=RHandler)
    thr = Thread(target = server.serve_forever, daemon = True)
    thr.start()
    return thr, server

if __name__ == '__main__':
    thr, server = create_server()
    print("\n\n***************************\n"
          f"Entrar a {myIP}:8000"
          "\n***************************\n\n")
    while RHandler.running: sleep(.1)
    server.server_close()
    server.shutdown()

