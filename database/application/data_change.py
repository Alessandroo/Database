from database.application.indexing_id import IndexId
from database.filework import file_worker
from database.utils.JSON import to_json
from database.utils.profiler import Profiler


def insert(database, table, data):
    if not isinstance(data, (list, tuple)) or len(data == 1):
        return insert_one(database, table, data)
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


def save():
    pass


def update(database, table, data):
    print("update")
    print(data)


def delete(database, table, data):
    print("delete")
    print(data)
