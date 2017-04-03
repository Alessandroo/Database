from database.filework.config_reader import get_config_parameter
from database.utils.JSON import from_json, to_json
import os


def write(database, table, data):
    enter_in_directory(database)
    filename = "{}.json".format(table)
    with open(filename, 'a') as file:
        for item in data:
            file.write('{}\n'.format(to_json(item)))


def read(database, table):
    enter_in_directory(database)
    filename = "{}.json".format(table)
    try:
        with open(filename) as file:
            data = []
            for line in file.readlines():
                data.append(from_json(line))
            return data
    except FileNotFoundError:
        print('Table {} in database {} does not exist'.format(table, database))


# дописать потом
def enter_in_directory(database):
    if os.name == 'nt':
        directory = "{}/{}".format(get_config_parameter("path"), database)
    elif os.name == 'posix':
        directory = "{}\{}".format(get_config_parameter("path"), database)
    try:
        os.makedirs(directory)
    except OSError:
        pass
    os.chdir(directory)
