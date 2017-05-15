import database.application.system_change as system_change
import database.application.triggers as triggers
import database.application.indexing as indexing
# import database.application.data_change as data_change
# import database.application.data_read as data_read


class FunctionInfo:
    def __init__(self, function_type, function_subtype=None):
        self.function_type = function_type
        self.function_subtype = function_subtype


_FUNCTIONS = {
    "createCollection": (system_change.create_collection, FunctionInfo("system")),
    "renameCollection": (system_change.rename_collection, FunctionInfo("system")),
    "dropCollection": (system_change.drop_collection, FunctionInfo("system")),
    "createDataBase": (system_change.create_database, FunctionInfo("system", "super")),
    "dropDataBase": (system_change.drop_database, FunctionInfo("system", "super")),
    "createTrigger": (triggers.create_trigger, FunctionInfo("trigger")),
    "deleteTrigger": (triggers.delete_trigger, FunctionInfo("trigger")),
    "createIndex": (indexing.create_index, FunctionInfo("index")),
    "deleteIndex": (indexing.delete_index, FunctionInfo("index")),
    "insert": (None, FunctionInfo("changing")),
    "save": (None, FunctionInfo("changing")),
    "update": (None, FunctionInfo("changing")),
    "delete": (None, FunctionInfo("changing")),
    "find": (None, FunctionInfo("reading")),
    "findOne": (None, FunctionInfo("reading")),
    "count": (None, FunctionInfo("reading")),
    "limit": (None, FunctionInfo("reading")),
    "skip": (None, FunctionInfo("reading")),
    "sort": (None, FunctionInfo("reading")),
    "distinct": (None, FunctionInfo("reading"))
}


def get_db_functions():
    return _FUNCTIONS
