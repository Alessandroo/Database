class FunctionInfo:
    def __init__(self, function_type, function_subtype):
        self.function_type = function_type
        self.function_subtype = function_subtype

_FUNCTIONS = {}


def db_function(name, function_type, function_subtype=None):
    def add(fn):
        _FUNCTIONS[name] = (fn, FunctionInfo(function_type, function_subtype))

    return add


def get_db_functions():
    return _FUNCTIONS
