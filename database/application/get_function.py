from database.utils.JSON import from_json, to_json
from database.application.data_worker import get_db_functions


def get_function(json):
    obj = from_json(json)
    function_mapper = get_db_functions()
    result = function_mapper[obj['function']](obj['database'], obj['collection'], obj['data'])
    print(result)


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
