import sys
import collections

from database.filework import file_worker
from database.filework.index_worker import get_indexes, set_indexes
from database.utils.JSON import to_json
from database.utils.exeptions import IndexNotExist
from database.utils.profiler import Profiler
from database.utils.singleton import SingletonByName

_FUNCTIONS = {}


class IndexId(metaclass=SingletonByName):
    def __init__(self, database, table):
        self.database = database
        self.table = table
        try:
            self.__data = get_indexes(database, table)
        except IndexNotExist:
            self.__data = {}

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        set_indexes(self.database, self.table, value)
        self.__data = value


def db_function(name):
    def add(fn):
        _FUNCTIONS[name] = fn

    return add


def get_db_functions():
    return _FUNCTIONS


@db_function("insert")
def insert(database, table, data):
    with Profiler() as prof:
        index = IndexId(database, table)
        _id = 0
        if index.data:
            max_id = max(list(index.data.keys()))
            _id = max_id + 1
        for i in range(len(data)):
            data[i]["_id"] = _id + i
        tells = file_worker.insert(database, table, data)
        for k, v in enumerate(tells):
            index.data[_id + k] = v
        # это необходимо для срабатывание setter, и записывания индекса в файл
        index.data = index.data
    return to_json({"time": prof.total_time, "result": "ok"})


@db_function("insertOne")
def insert_one(database, table, data):
    with Profiler() as prof:
        index = IndexId(database, table)
        _id = 0
        if index.data:
            max_id = max(list(index.data.keys()))
            _id = max_id + 1
        data["_id"] = _id
        index.data[_id] = file_worker.insert_one(database, table, data)
        # это необходимо для срабатывание setter, и записывания индекса в файл
        index.data = index.data
    return to_json({"time": prof.total_time, "result": "ok"})


@db_function("find")
def find(database, table, data):
    with Profiler() as prof:
        search = data["search"]
        output_rule = data["output rule"]
        if not (search or output_rule):
            output = file_worker.find_all(database, table)
        if "_id" in search:
            index = IndexId(database, table)
            if isinstance(search["_id"], collections.Iterable):
                # insert try except KeyError
                index_tail = list(map(lambda key: index[key], search["_id"]))
            else:
                index_tail = [index[search["_id"]]]
            output = file_worker.find_by_index_id



@db_function("findOne")
def find_one():
    print()


@db_function("save")
def save():
    pass


@db_function("update")
def update(database, table, data):
    print("update")
    print(data)


@db_function("remove")
def delete(database, table, data):
    print("delete")
    print(data)


@db_function("count")
def count():
    pass


@db_function("limit")
def limit():
    pass


@db_function("skip")
def skip():
    pass


@db_function("sort")
def sort():
    pass


@db_function("distinct")
def distinct():
    pass


@db_function("createCollection")
def create_collection(database, table):
    pass


@db_function("renameCollection")
def rename_collection():
    pass


@db_function("drop")
def drop_collection():
    pass


@db_function("dropDataBase")
def drop_database():
    pass


if __name__ == '__main__':
    list1 = {}
    print("via Dict")
    with Profiler():
        for i in range(int(1e7)):
            list1[i] = 10 * i
    print("get Elem")
    with Profiler():
        print(list1[int(1e6 + 1)])
    # list2 = []
    # print("via Tuple")
    # with Profiler():
    #     for i in range(int(1e7)):
    #         list2.append((i, i * 10))
    # print("get Elem")
    # with Profiler():
    #     print(list2[list2.index((int(1e6 + 1), int(1e6 + 1)*10))])

    print('size ' + str(sys.getsizeof(list1) / 2 ** 20))
    # print('size ' + str(sys.getsizeof(list2) / 2 ** 10))
