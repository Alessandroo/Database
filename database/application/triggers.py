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


def create_trigger(database, collection, type_trigger, data):
    if type_trigger in ["unique", "auto increment", "custom", "constraint", "check type", "not null"]:
        if type_trigger == "unique":
            field = data["field"]
            return triggers.create_unique_trigger(database, collection, field)
        elif type_trigger == "auto increment":
            field = data["field"]
            return triggers.create_auto_increment_trigger(database, collection, field)
        elif type_trigger == "custom":
            situation = data["situation"]
            parameters = data["parameters"]
            code = data["code"]
            if data["action"]:
                action = data["action"]
                return triggers.create_custom_trigger(database, collection, situation, parameters, code, action)
            else:
                return triggers.create_custom_trigger(database, collection, situation, parameters, code)
        elif type_trigger == "constraint":
            field = data["field"]
            parent_collection = data["parent"]["collection"]
            parent_field = data["parent"]["field"]
            return triggers.create_constraint_trigger(database, collection, field, parent_collection, parent_field)
        elif type_trigger == "check type":
            valid_types = ["object", "string", "float", "int", "array", "bool"]
            field = data["field"]
            types_of_object = data["object types"]
            if set(types_of_object) <= set(valid_types):
                pass
            return triggers.create_check_type_trigger(database, collection, field, types_of_object)
        else:
            field = data["field"]
            return triggers.create_not_null_trigger(database, collection, field)
    else:
        return Answer("Invalid query", error=True)


def delete_trigger(database, collection, type_trigger, data):
    pass


if __name__ == '__main__':
    trig = Trigger()
    print(trig.__dict__)
