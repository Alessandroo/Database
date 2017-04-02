from database.filework.config_reader import get_config_parameter
from database.utils.JSON import from_json, to_json


def write(database, table, data):
    # path = get_config_parameter("path")
    # print(path)
    filename = "{}.json".format(table)
    with open(filename, 'a') as file:
        for item in data:
            file.write('{}\n'.format(to_json(item)))


def read(database, table):
    filename = "{}/{}/{}".format(get_config_parameter("path"), database, table)
    try:
        with open(filename) as file:
            data = []
            for line in file.readlines():
                data.append(from_json(line))
            return data
    except FileNotFoundError:
        print('Table {} in database {} does not exist'.format(table, database))