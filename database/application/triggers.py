import database.filework.triggers as triggers
from database.utils.answer import Answer


class Field:
    def __init__(self, database, collection, field):
        self._database = database
        self._collection = collection
        self._field = field

    @property
    def database(self):
        return self.database()

    @property
    def collection(self):
        return self._collection

    @property
    def field(self):
        return self._field


class Trigger:
    def __init__(self):
        self._unique = None
        self._autoincrement = None
        self._custom = None
        self._constraint = None
        self._check_type = None
        self._not_null = None

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, value):
        self._unique = value

    @unique.getter
    def unique(self):
        return self._unique

    @property
    def autoincrement(self):
        return self._autoincrement

    @autoincrement.setter
    def autoincrement(self, value):
        self._autoincrement = value

    @autoincrement.getter
    def autoincrement(self):
        return self._autoincrement

    @property
    def custom(self):
        return self._custom

    @custom.setter
    def custom(self, value):
        self._custom = value

    @custom.getter
    def custom(self):
        return self._custom

    @property
    def constraint(self):
        return self._constraint

    @constraint.setter
    def constraint(self, value):
        self._constraint = value

    @constraint.getter
    def constraint(self):
        return self._constraint

    @property
    def check_type(self):
        return self._check_type

    @check_type.setter
    def check_type(self, value):
        self._check_type = value

    @check_type.getter
    def check_type(self):
        return self._check_type

    @property
    def not_null(self):
        return self._not_null

    @not_null.setter
    def not_null(self, value):
        self._not_null = value

    @not_null.getter
    def not_null(self):
        return self._not_null


def create_trigger(database, collection, type_trigger, data_row, data):
    if type_trigger in ["unique", "auto increment", "custom", "constraint", "check type", "not null"]:
        if type_trigger == "unique":
            field = data_row["field"]
            return triggers.create_unique_trigger(database, collection, field, data=data)
        elif type_trigger == "auto increment":
            field = data_row["field"]
            return triggers.create_auto_increment_trigger(database, collection, field, data=data)
        elif type_trigger == "custom":
            name = data_row["name"]
            situation = data_row["situation"]
            parameters = data_row["parameters"]
            code = data_row["code"]
            if data_row["action"]:
                actions = data_row["actions"]
                actions_on_true = None
                actions_on_false = None
                if actions["on true"]:
                    actions_on_true = actions["on true"]
                if actions["on false"]:
                    actions_on_false = actions["on false"]
                return triggers.create_custom_trigger(name, database, collection, situation, parameters, code,
                                                      actions_on_true=actions_on_true,
                                                      actions_on_false=actions_on_false,
                                                      data=data)
            else:
                return triggers.create_custom_trigger(name, database, collection, situation, parameters, code,
                                                      data=data)
        elif type_trigger == "constraint":
            name = data_row["name"]
            field = data_row["field"]
            parent_collection = data_row["parent"]["collection"]
            parent_field = data_row["parent"]["field"]
            return triggers.create_constraint_trigger(name, database, collection, field, parent_collection,
                                                      parent_field, data=data)
        elif type_trigger == "check type":
            valid_types = ["object", "string", "float", "int", "array", "bool"]
            field = data_row["field"]
            types_of_object = data_row["object types"]
            if set(types_of_object) <= set(valid_types):
                return triggers.create_check_type_trigger(database, collection, field, types_of_object, data=data)
        elif type_trigger == "not null":
            field = data_row["field"]
            return triggers.create_not_null_trigger(database, collection, field, data=data)
    return Answer("Invalid query", error=True)


def delete_trigger(database, collection, type_trigger, data_row, data):
    if type_trigger == "custom":
        name = data_row["name"]
        situation = data_row["situation"]
    elif type_trigger == "constraint":
        name = data_row["name"]
        situation = None
    else:
        name = None
        situation = None
    field = data_row["field"]
    return triggers.delete_trigger(database, collection, type_trigger, field, name, situation, data)


if __name__ == '__main__':
    data = triggers.read_db_file("warsaw")
    print(data)
    print(create_trigger("warsaw", "lodz", "not null", {"field": "name"},data))