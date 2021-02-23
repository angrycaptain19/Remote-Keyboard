from threading import Thread
from http.server import HTTPServer
from Handler import RHandler, update_html, resource_path
from time import sleep
from socket import gethostname, gethostbyname

myIP = gethostbyname(gethostname())
RHandler.IP = myIP
update_html(RHandler)

def create_server(port = 8000) -> tuple[Thread, HTTPServer]:
    server = HTTPServer(server_address=('', port), RequestHandlerClass=RHandler)
    thr = Thread(target = server.serve_forever, daemon = True)
    thr.start()
    return thr, server

def print_instructions():
    with open (resource_path(".\\Instructions.txt"), 'rb') as file: text = file.read()
    print(text.decode('utf-8'))

if __name__ == '__main__':
    thr, server = create_server()
    print_instructions()
    print(f"IP:Puerto --> {myIP}:8000\n")

    while RHandler.running: sleep(.1)
    server.server_close()
    server.shutdown()

