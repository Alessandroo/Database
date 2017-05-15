from database.application.indexing import create_index
from database.filework.file_worker import read_db_file, write_db_file
from database.utils.answer import Answer
from database.utils.exceptions import DatabaseNotExist


def create_unique_trigger(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "unique", data)
        data["collections"][collection]["triggers"]["unique"][field] = True
        return create_index(database, collection, field, data)
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)


def create_auto_increment_trigger(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "auto increment", data)
        data["collections"][collection]["triggers"]["auto increment"][field] = True
        return create_index(database, collection, field, data)
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)


def create_custom_trigger(name, database, collection, situation, parameters, code, actions_on_true=None,
                          actions_on_false=None, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "custom", data)
        if situation not in data["collections"][collection]["triggers"]["custom"]:
            data["collections"][collection]["triggers"]["custom"][situation] = {}
        data["collections"][collection]["triggers"]["custom"][situation][name] = {"code": code,
                                                                                  "parameters": parameters,
                                                                                  "actions": {"true": actions_on_true,
                                                                                              "false": actions_on_false}}
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_constraint_trigger(name, database, collection, field, parent_collection, parent_field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "constraint", data)
        data["collections"][collection]["triggers"]["constraint"][name] = {"field": field,
                                                                           "parent": {"location": parent_collection,
                                                                                      "field": parent_field}}
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_check_type_trigger(database, collection, field, types_of_object, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "check type", data)
        data["collections"][collection]["triggers"]["check type"][field] = types_of_object
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_not_null_trigger(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data = create_trigger_dict(collection, "not null", data)
        data["collections"][collection]["triggers"]["not null"][field] = True
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def delete_trigger(database, collection, type_trigger, field, name=None, situation=None, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)

    if data["collections"] and collection in data["collections"]:
        if data["collections"][collection]["triggers"] and type_trigger in data["collections"][collection]["triggers"]:
            if type_trigger == "custom":
                try:
                    data["collections"][collection]["triggers"]["custom"][situation].pop(name)
                except KeyError:
                    pass

            elif type_trigger == "constraint":
                try:
                    data["collections"][collection]["triggers"]["constraint"].pop(name)
                except KeyError:
                    pass

            else:
                try:
                    data["collections"][collection]["triggers"][type_trigger].pop(field)
                except KeyError:
                    pass
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)

    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_trigger_dict(collection, type_trigger, data):
    if "triggers" not in data["collections"][collection]:
        data["collections"][collection]["triggers"] = {}
        data["collections"][collection]["triggers"][type_trigger] = {}
    return data


if __name__ == '__main__':
    pass
