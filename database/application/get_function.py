import database.application.data_change
import database.application.data_read
import database.application.system_change

from database.application.data_worker import get_db_functions
from database.utils.JSON import to_json


def get_function(instruction):
    # obj = from_json(json)
    function_mapper = get_db_functions()
    result = function_mapper
    # result = function_mapper[instruction['function']](instruction['database'], instruction['collection'], instruction['data'])
    print(result)
    return "ok"


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
    data.function = 'insert'
    data.database = 'london'
    data.collection = 'people'
    data.data = [Ment("lol", 18).__dict__, Ment("lolita", 27).__dict__]
    get_function(to_json(data.__dict__))
