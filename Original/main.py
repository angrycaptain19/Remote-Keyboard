from threading import Thread
from http.server import HTTPServer
from Handler.Handler import RHandler, update_html
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

if __name__ == '__main__':
    thr, server = create_server()
    print(f"Entrar a {myIP}:8000")
    while RHandler.running: sleep(.1)
    server.server_close()
    server.shutdown()

