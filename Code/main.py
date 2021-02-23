from http.server import HTTPServer
from Handler import RHandler, update_ip, resource_path
from socket import gethostname, gethostbyname

myIP = gethostbyname(gethostname())
RHandler.IP = myIP
update_ip(RHandler)

def print_instructions():
    with open (resource_path(".\\Instructions.txt"), 'rb') as file: text = file.read()
    print(text.decode('utf-8'))

if __name__ == '__main__':
    server = HTTPServer(server_address=('', 8000), RequestHandlerClass=RHandler)
    print_instructions()
    print(f"IP:Puerto --> {myIP}:8000\n")

    while RHandler.running: server.handle_request()
    server.server_close()
