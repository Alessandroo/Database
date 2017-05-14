from database.utils.JSON import to_json
from database.application.function_mapper import get_db_functions
from database.utils.answer import Answer


def check_super_system_function(name):
    function_mapper = get_db_functions()
    function_info = function_mapper[name]
    if function_info[1].function_type == "system" and function_info[1].function_subtype == "super":
        return True
    else:
        return False


def get_database_name(instruction):
    function_mapper = get_db_functions()
    function_info = function_mapper[instruction["function"]]
    if function_info[1].function_type == "system":
        return instruction["data"]["database"]
    else:
        return instruction["database"]


def check_the_validity_of_the_instruction(instruction):
    return True


def execute_instruction(instruction):
    function_mapper = get_db_functions()
    print("function_mapper")
    print(function_mapper)
    print('instruction["function"]')
    print(instruction["function"])
    if not instruction["function"] is None and instruction["function"] in function_mapper:
        function_info = function_mapper[instruction["function"]]
    else:
        return Answer("Check command {}".format(instruction["function"])).info
    print("function_info")
    print(function_info)
    if function_info[1].function_type == "system":
        print('instruction["data"]')
        print(instruction["data"])
        result = function_info[0](instruction["data"])
        return result
    elif function_info[1].function_type == "trigger":
        result = function_info[0](instruction["database"], instruction["collection"], instruction["type"],
                                  instruction["data"]
                                  )
        return result
    elif function_info[1].function_type == "index":
        result = function_info[0](instruction["database"], instruction["collection"], instruction["field"])
        return result
    else:
        result = function_info[0](instruction["database"], instruction["collection"], instruction["data"])
        return result


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
    execute_instruction(to_json(data.__dict__))
