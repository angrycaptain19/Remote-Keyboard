from http.server import HTTPServer
from Handler import RHandler, update_ip, resource_path
from socket import gethostname, gethostbyname

def print_instructions():
    with open (resource_path(".\\Instructions.txt"), 'rb') as file: text = file.read()
    print(text.decode('utf-8'))

if __name__ == '__main__':

    # Gets local IP
    myIP = gethostbyname(gethostname())
    RHandler.IP = myIP
    update_ip(RHandler)

    # Creates server
    server = HTTPServer(server_address=('', 8000), RequestHandlerClass=RHandler)

    # Console output
    print_instructions()
    print(f"IP:Puerto --> {myIP}:8000\n")

    # Loops until 'Exit' is pressed
    while RHandler.running: server.handle_request()
    server.server_close()
