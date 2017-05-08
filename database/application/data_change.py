from database.application.indexing import IndexId
from database.filework import file_worker
from database.utils.JSON import to_json
from database.utils.profiler import Profiler


@db_function("insert", "changing")
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


@db_function("insertOne", "changing")
def insert_one(self, database, table, data):
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


@db_function("save", "changing", "pop")
def save():
    pass


@db_function("update", "changing")
def update(database, table, data):
    print("update")
    print(data)


@db_function("remove", "changing")
def delete(database, table, data):
    print("delete")
    print(data)
