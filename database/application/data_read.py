import collections

from database.application.function_mapper import db_function
from database.application.indexing import IndexId
from database.filework import file_worker
from database.utils.profiler import Profiler


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
@db_function("find", "reading")
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


@db_function("findOne", "reading")
def find_one():
    print()


@db_function("count", "calculating")
def count():
    pass


@db_function("limit", "calculating")
def limit():
    pass


@db_function("skip", "calculating")
def skip():
    pass


@db_function("sort", "calculating")
def sort():
    pass


@db_function("distinct", "calculating")
def distinct():
    pass
