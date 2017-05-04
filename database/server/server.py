import threading

import zmq

from database.application.get_function import get_function
from database.utils.JSON import from_json
from database.utils.check_license import valid_license


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind('tcp://127.0.0.1:43000')
        while True:
            instruction = socket.recv_string()
            instruction = from_json(instruction)
            # TODO: delete
            print(instruction)
            if instruction == "stop":
                break
            result = get_function(instruction)
            socket.send_string(result)
        socket.close()


if __name__ == '__main__':
    if valid_license():
        serv = Server()
        serv.start()
