from database.utils.recursive_dict import RecDict

_FUNCTIONS = RecDict()


def db_function(name, function_type, function_subtype=None):
    print(name)
    def add(fn):
        if function_subtype is None:
            _FUNCTIONS[function_type][name] = fn
        else:
            _FUNCTIONS[function_type][function_subtype][name] = fn

    return add


def get_db_functions():
    return _FUNCTIONS
