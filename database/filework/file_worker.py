import os

import bson

from database.filework.config_reader import get_config_parameter
from database.utils.exceptions import DatabaseNotExist


def insert(database, table, data):
    old_directory = os.getcwd()
    enter_in_directory(database)
    filename = "{}.bs".format(table)
    with open(filename, 'a') as file:
        tell = []
        for item in data:
            tell.append(file.tell())
            file.write('{}\n'.format(bson.dumps(item)))
    os.chdir(old_directory)
    return tell


def insert_one(database, table, data):
    old_directory = os.getcwd()
    enter_in_directory(database)
    filename = "{}.bs".format(table)
    with open(filename, 'a') as file:
        tell = file.tell()
        file.write('{}\n'.format(bson.dumps(data)))
    os.chdir(old_directory)
    return tell


def find_all(database, table):
    old_directory = os.getcwd()
    enter_in_directory(database)
    filename = "{}.bs".format(table)
    try:
        with open(filename) as file:
            data = []
            for line in file.readlines():
                data.append(bson.loads(line))
            return data
    except FileNotFoundError:
        # переделать
        print('Table {} in database {} does not exist'.format(table, database))
    finally:
        os.chdir(old_directory)


def find(database, table, search, output_rule):
    pass


def enter_in_system_directory():
    os.chdir(get_config_parameter("path"))


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
        try:
            data_to_write = bson.dumps(data_to_write)
        except (IndexError, bson.struct.error):
            os.chdir(old_directory)
            raise DatabaseNotExist("Database {} does not exit or corrupted".format(database))
        if os.path.isfile("system.bs"):
            with open('system.bs', 'wb') as file_to_write:
                file_to_write.write(data_to_write)
            os.chdir(old_directory)
            return
    os.chdir(old_directory)
    raise DatabaseNotExist("Database {} does not exit or corrupted".format(database))
