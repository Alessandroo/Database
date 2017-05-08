import database.application.system_change as system_change
import database.application.triggers as triggers


class FunctionInfo:
    def __init__(self, function_type, function_subtype=None):
        self.function_type = function_type
        self.function_subtype = function_subtype


_FUNCTIONS = {
    "createCollection": (system_change.create_collection, FunctionInfo("system")),
    "renameCollection": (system_change.rename_collection, FunctionInfo("system")),
    "dropCollection": (system_change.drop_collection, FunctionInfo("system")),
    "createDataBase": (system_change.create_database, FunctionInfo("system")),
    "dropDataBase": (system_change.drop_database, FunctionInfo("system")),
    "createTrigger": (triggers.create_trigger, FunctionInfo("trigger")),
    "deleteTrigger": (triggers.delete_trigger, FunctionInfo("trigger"))
}


def get_db_functions():
    return _FUNCTIONS
