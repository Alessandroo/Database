from database.utils.JSON import from_json, to_json
from database.application.data_worker import *

function_mapper = {'create': create, 'read': read, 'update': update, 'delete': delete}


def get_function(json):
    obj = from_json(json)
    function_mapper[obj['function']](obj['database'], obj['collection'], obj['data'])


if __name__ == '__main__':
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


    data = DataStructure()
    data.function = 'create'
    data.database = 'models'
    data.collection = 'people'
    data.data = Ment("lol", 18).__dict__
    get_function(to_json(data.__dict__))
