import threading

import zmq

from database.application.function_mapper import get_db_functions
from database.application.function_parser import execute_instruction, check_super_system_function, \
    check_the_validity_of_the_instruction
from database.filework.system_change import get_databases
from database.utils.JSON import from_json
from database.utils.answer import Answer
from database.utils.check_license import valid_license
from multiprocessing import Process

class Database:
    def __init__(self, name, port, process):
        self.name = name
        self.port = port
        self.process = process

class DatabaseServer(Process):
    def __init__(self, database, port):
        Process.__init__(self)
        self.database = database
        self.port = port
        self.work = True

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:{}".format(self.port))
        while self.work:
            instruction = socket.recv_string()
            instruction = from_json(instruction)
            # TODO: delete
            print(instruction)
            result = execute_instruction(instruction)
            socket.send_string(result)
        socket.close()

    def stop(self):
        self.work = False

    def is_work(self):
        return self.is_alive()


class ServerTask(threading.Thread):
    def __init__(self, port, count_workers):
        threading.Thread.__init__(self)
        self.port = port
        self.count_workers = count_workers

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://127.0.0.1:{}'.format(self.port))

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        condition = threading.Condition()
        databases = {}
        for name, port in get_databases().items():
            temp = DatabaseServer(name, port)
            temp.start()
            databases[name] = Database(name, port, temp)

        for i in range(self.count_workers):
            ServerWorker(context, condition, databases).start()

        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    def __init__(self, context, condition, database):
        threading.Thread.__init__(self)
        self.context = context
        self.condition = condition
        self.database = database

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        while True:
            instruction = worker.recv_string()
            instruction = from_json(instruction)
            if not check_the_validity_of_the_instruction(instruction):
                worker.send_string("Invalid instruction syntax")
            if not self.condition.acquire(False):
                with self.condition:
                    self.condition.wait()
            if check_super_system_function(instruction["function"]):





# class Server(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         context = zmq.Context()
#         socket = context.socket(zmq.REP)
#         socket.bind('tcp://127.0.0.1:43000')
#         while True:
#             instruction = socket.recv_string()
#             instruction = from_json(instruction)
#             # TODO: delete
#             print(instruction)
#             result = get_function(instruction)
#             socket.send_string(result)
#         socket.close()


if __name__ == '__main__':
    if valid_license():
        serv = Server()
        serv.start()
