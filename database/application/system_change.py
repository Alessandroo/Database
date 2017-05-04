import os

import bson

from database.filework.file_worker import enter_in_system_directory
from database.utils.function_mapper import db_function


class Answer:
    def __init__(self, info):
        self.info = info

    def __repr__(self):
        return self.info


@db_function("createCollection", "system")
def create_collection(database, table):
    pass


@db_function("renameCollection", "system")
def rename_collection():
    pass


@db_function("drop", "system")
def drop_collection():
    pass


@db_function("createDataBase", "system")
def create_database(data_row):
    database = data_row["database"]
    old_directory = os.getcwd()
    enter_in_system_directory()
    if os.path.isfile("system.bs"):
        with open("system.bs", 'rb') as file:
            try:
                data = bson.loads(file.read())
            except (IndexError, bson.struct.error):
                print("The file with the signature of database is corrupted")
                os.chdir(old_directory)
                return Answer("Error The file with the signature of database is corrupted")
            if database in data:
                os.chdir(old_directory)
                return Answer('Database {} already exist'.format(database))
            data[database] = {}
    else:
        data = {database: {}}
    if not os.path.isdir(database):
        if os.path.exists(database):
            return Answer('{} already exist, but it is not directory'.format(database))
        else:
            os.makedirs(database)
    with open('system.bs', 'wb') as file_to_write:
        file_to_write.write(bson.dumps(data))
    os.chdir(old_directory)
    print("databases")
    print(data)
    return Answer("Operation finished")


@db_function("dropDataBase", "system")
def drop_database(data_row):
    database = data_row["database"]
    old_directory = os.getcwd()
