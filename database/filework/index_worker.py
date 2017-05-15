import os
import pickle

from database.filework.file_worker import enter_in_directory
from database.utils.exceptions import IndexNotExist


def get_indexes(database, table):
    old_directory = os.getcwd()
    enter_in_directory(database)
    filename = "{}.index".format(table)
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            return data
    except FileNotFoundError:
        raise IndexNotExist
    finally:
        os.chdir(old_directory)


def set_indexes(database, table, data):
    old_directory = os.getcwd()
    enter_in_directory(database)
    filename = "{}.index".format(table)
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol=0)
    os.chdir(old_directory)


if __name__ == '__main__':
    set_indexes("users", {0: 0})
    d = get_indexes("london", "people")
    print(d)
