_FUNCTIONS = {}

def db_function(name):
    def add(fn):
        _FUNCTIONS[name] = fn

    return add


def get_db_functions():
    return _FUNCTIONS
