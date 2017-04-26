import socket

working = True
HOST = ''
PORT = 9090


def stop():
    working = False


def start_server():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print('Connected:', addr)
    while True:
        client_request = conn.recv(1024)
        if not client_request:
            break
        print('Recieved message:', client_request)
    conn.close()
if __name__ == '__main__':
    while working:
        start_server()
