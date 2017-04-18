import os

import bson

from database.filework.config_reader import get_config_parameter
from database.utils.JSON import from_json


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


# дописать потом
def enter_in_directory(database):
    if os.name == 'nt':
        directory = "{}/{}".format(get_config_parameter("path"), database)
    elif os.name == 'posix':
        directory = "{}\{}".format(get_config_parameter("path"), database)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)
