import zmq

from database.utils.JSON import to_json


class Ment:
    def __init__(self, name="alex", age=15):
        self.name = name
        self.age = age
        self.language = ["greece", "spanish", "english"]


class DataStructure:
    def __init__(self):
        self.function = None
        self.data = None
        self.database = None
        self.collection = None


def start_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:43000')

    data = DataStructure()
    # data.function = 'insert'
    # data.database = 'london'
    # data.collection = 'people'
    # data.data = [Ment("lol", 18).__dict__, Ment("lolita", 27).__dict__]
    # data.function = 'renameCollection'
    data.function = 'dropCollection'
    data.data = {"database": "poland", "collection": "lodz", "login": "Alex", "password": "Alex"}
    # data.data = {"database": 'poland', 'table': {'old': 'belostock', 'new': 'belostock'}}

    socket.send_string(to_json(data))
    # if socket.recv_string():
    print(socket.recv_string())


if __name__ == '__main__':
    start_client()

    # if __name__ == '__main__':
    #     class Ment:
    #         def __init__(self, name="alex", age=15):
    #             self.name = name
    #             self.age = age
    #             self.language = ["greece", "spanish", "english"]
    #
    #
    #     class DataStructure:
    #         def __init__(self):
    #             self.function = None
    #             self.data = None
    #             self.database = None
    #             self.collection = None
    #
    #
    #     data = DataStructure()
    #     data.function = 'insert'
    #     data.database = 'london'
    #     data.collection = 'people'
    #     data.data = [Ment("lol", 18).__dict__, Ment("lolita", 27).__dict__]
    #     receive_data = to_json(data.__dict__).encode("UTF-8")
    #     socket_server = socket.socket()
    #     socket_server.connect(SERVER_ADDR)
    #     socket_server.send(receive_data)
    #     while True:
    #         socket_server.send(receive_data)
    #     socket_server.close()
