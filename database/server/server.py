import threading
from multiprocessing import Process

import zmq

from database.application.function_parser import execute_instruction, check_super_system_function, \
    check_the_validity_of_the_instruction, get_database_name
from database.filework.system_change import get_databases
from database.utils.JSON import from_json, to_json
from database.utils.answer import Answer
from database.utils.check_license import valid_license


class Database:
    def __init__(self, name, port, process):
        self.name = name
        self.port = port
        self.process = process


class DatabaseServer(Process):
    def __init__(self, database, port):
        print("{} init".format(database))
        super().__init__()
        self.database = database
        self.port = port
        self.work = True

    def run(self):
        print("{} run".format(self.database))
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://127.0.0.1:{}".format(self.port))
        while self.work:
            instruction = from_json(socket.recv_string())
            # instruction = from_json(instruction)
            # TODO: delete
            # print(instruction)
            result = execute_instruction(instruction)
            # result = Answer(instruction["function"])
            socket.send_string(to_json(result))
        socket.close()

    def stop(self):
        self.work = False

    def is_work(self):
        return self.is_alive()


class ServerTask(threading.Thread):
    def __init__(self, databases, port, count_workers):
        super().__init__()
        self.databases = databases
        self.port = port
        self.count_workers = count_workers

    def start(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://127.0.0.1:{}'.format(self.port))

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        works = {}
        event = threading.Event()
        event.set()

        for i in range(self.count_workers):
            ServerWorker(context, works, event, self.databases).start()

        zmq.proxy(frontend, backend)
        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    def __init__(self, context, works, event, databases):
        threading.Thread.__init__(self)
        self.context = context
        self.works = works
        self.event = event
        self.databases = databases

    def run(self):
        print("{} run".format(self.getName()))
        worker = self.context.socket(zmq.REP)
        worker.connect('inproc://backend')
        while True:
            instruction = worker.recv_string()
            # print(instruction)
            instruction = from_json(instruction)
            if not check_the_validity_of_the_instruction(instruction):
                worker.send_string("Invalid instruction syntax")
            if check_super_system_function(instruction["function"]):
                if not self.event.is_set():
                    self.event.wait()
                self.event.clear()
                if self.works:
                    while True in self.works.values():
                        self.event.wait(1)
                result = execute_instruction(instruction)
                if not result.error:
                    if instruction["function"] == "createDataBase":
                        name = get_database_name(instruction)
                        port = instruction["data"]["port"]
                        temp = DatabaseServer(name, port)
                        temp.start()
                        self.databases[instruction["data"]["database"]] = Database(name, port, temp)
                    elif instruction["function"] == "dropDataBase":
                        name = get_database_name(instruction)
                        if name in self.databases:
                            database_info = self.databases.pop(name)
                            database_server = database_info.process
                            database_server.stop()
                worker.send_string(result.info)
                self.event.set()
            else:
                if not self.event.is_set():
                    self.event.wait()
                self.works[self.getName()] = True
                name = get_database_name(instruction)
                if name in self.databases:
                    context = zmq.Context()
                    receiver = context.socket(zmq.REQ)
                    receiver.connect('tcp://127.0.0.1:{}'.format(self.databases[name].port))
                    receiver.send_string(to_json(instruction))
                    result = from_json(receiver.recv_string())
                    receiver.close()
                    # print("result")
                    # print(result["_info"])
                    worker.send_string(result["info"])
                else:
                    worker.send_string("Invalid instruction syntax")
                self.works[self.getName()] = False


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
        databases = {}
        print("databases {}".format(get_databases()))
        for name, port in get_databases().items():
            temp = DatabaseServer(name, port)
            temp.start()
            databases[name] = Database(name, port, temp)
        serv = ServerTask(databases, 50000, 3)
        serv.start()
