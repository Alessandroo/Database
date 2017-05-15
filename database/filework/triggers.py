import os

import bson

from database.filework.file_worker import enter_in_system_directory
from database.utils.answer import Answer
from database.utils.exceptions import DatabaseNotExist
from database.application.indexing import create_index


def create_unique_trigger(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data["collections"][collection]["triggers"]["unique"][field] = types_of_object
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_auto_increment_trigger(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data["collections"][collection]["triggers"]["auto increment"][field] = True
        return create_index(database, collection, field, data)
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)


def create_custom_trigger(name, database, collection, situation, parameters, code, action=None, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
        data["collections"][collection]["triggers"]["types_of_object"][field] = types_of_object
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def create_constraint_trigger(name, database, collection, field, parent_collection, parent_field, data= None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    if data["collections"] and collection in data["collections"]:
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
        data["collections"][collection]["triggers"]["not null"][field] = True
    else:
        return Answer('Collection {} of database {} does not exist'.format(collection, database),
                      error=True)
    try:
        write_db_file(database, data)
    except DatabaseNotExist as e:
        return Answer(e.__str__(), error=True)
    return Answer("Operation finished")


def delete_trigger(database, collection, type_trigger, name, data=None):
    pass


def read_db_file(database):
    old_directory = os.getcwd()
    enter_in_system_directory()
    if os.path.isdir(database):
        os.chdir(database)
        if os.path.isfile("system.bs"):
            with open("system.bs", 'rb') as file:
                try:
                    data = bson.loads(file.read())
                except (IndexError, bson.struct.error):
                    os.chdir(old_directory)
                    raise DatabaseNotExist(
                        "Error The file with the signature of database {} is corrupted".format(database))
                os.chdir(old_directory)
                return data
    os.chdir(old_directory)
    raise DatabaseNotExist("Database {} does not exit or corrupted".format(database))


def write_db_file(database, data_to_write):
    old_directory = os.getcwd()
    enter_in_system_directory()
    if os.path.isdir(database):
        os.chdir(database)
        if os.path.isfile("system.bs"):
            with open('system.bs', 'wb') as file_to_write:
                file_to_write.write(data_to_write)
            os.chdir(old_directory)
            return
    os.chdir(old_directory)
    raise DatabaseNotExist("Database {} does not exit or corrupted".format(database))