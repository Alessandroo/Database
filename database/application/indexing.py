from database.filework.indexing import create_btree_index, create_unique_index, delete_index as delete_index_from_file
from database.filework.file_worker import read_db_file, write_db_file
from database.utils.answer import Answer
from database.utils.exceptions import DatabaseNotExist


def create_index(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        if data["collections"][collection]["triggers"]:
            if data["collections"][collection]["triggers"]["auto increment"] and \
                    data["collections"][collection]["triggers"]["auto increment"][field]:
                result = create_unique_index(database, collection, field, data, ("int",))
                if result.error:
                    data["collections"][collection]["triggers"]["auto increment"].pop(field)
                    write_db_file(database, data)
                    return result
                return result

            if data["collections"][collection]["triggers"]["unique"] and \
                    data["collections"][collection]["triggers"]["unique"][field]:
                if data["collections"][collection]["triggers"]["check type"] and \
                        data["collections"][collection]["triggers"]["check type"][field]:
                    result = create_unique_index(database, collection, field, data,
                                                 data["collections"][collection]["triggers"]["check type"][field])
                else:
                    result = create_unique_index(database, collection, field, data)
                if result.error:
                    data["collections"][collection]["triggers"]["unique"].pop(field)
                    write_db_file(database, data)
                    return result
                return result

            if data["collections"][collection]["triggers"]["check type"] and \
                    data["collections"][collection]["triggers"]["check type"][field]:
                if {"float", "int", "bool"}.isdisjoint(
                        set(data["collections"][collection]["triggers"]["check type"][field])):
                    return Answer('Indexing of field {} of collection {} in database {} is no use',
                                  error=True)
                else:
                    return create_btree_index(database, collection, field, data, list(
                        {"string", "float", "int", "bool"} & set(
                            data["collections"][collection]["triggers"]["check type"][field])))
        return create_btree_index(database, collection, field, data)
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)


def delete_index(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        if not (data["collections"][collection] and "indexes" in data["collections"][collection] and
                    data["collections"][collection]["indexes"] and field in data["collections"][collection]["indexes"]):
            return Answer("Field {} in collection {} of {} is not indexing".format(field, collection, database),
                          error=True)
        if data["collections"][collection] and "triggers" in data["collections"] and data["collections"][collection] \
                ["triggers"]:
            if "unique" in data["collections"][collection]["triggers"] and data["collections"][collection]["triggers"] \
                    ["unique"] and field in data["collections"][collection]["triggers"]["unique"]:
                return Answer(
                    "There exists a trigger 'unique' on the field {} in collection {} of {}".format(field, collection,
                                                                                                    database),
                    error=True)
            if "auto increment" in data["collections"][collection]["triggers"] and \
                    data["collections"][collection]["triggers"]["auto increment"] and \
                    field in data["collections"][collection]["triggers"]["auto increment"]:
                return Answer(
                    "There exists a trigger 'autoincrement' on the field {} in collection {} of {}".format(field,
                                                                                                           collection,
                                                                                                           database),
                    error=True)
        return delete_index_from_file(database, collection, field, data)
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)


if __name__ == '__main__':
    pass
