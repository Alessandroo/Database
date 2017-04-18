class SingletonByName(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if args not in cls._instances.keys():
            cls._instances[args] = super(SingletonByName, cls).__call__(*args, **kwargs)
        return cls._instances[args]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        database[name] = self.data



database = {}


if __name__ == '__main__':
    a, b, c = Logger("apple", "aa"), Logger("banana", 15), Logger("apple", "ss")
    a.name = "ananias"
    SingletonByName._instances[("ananias", "aa")] = SingletonByName._instances.pop(("apple", "aa"))
    print(a.name)
    print(SingletonByName._instances)
    print(database)
