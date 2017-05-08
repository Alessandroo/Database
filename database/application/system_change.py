import database.filework.system_change as system_change
from database.utils.answer import Answer


def create_collection(data_row):
    database = data_row["database"]
    collection = data_row["collection"]
    if "login" not in data_row and "password" not in data_row:
        return Answer("Login and password should be entered", error=True)
    login = data_row["login"]
    password = data_row["password"]
    return system_change.create_collection(database, collection, login, password)


def rename_collection(data_row):
    database = data_row["database"]
    collection = data_row["collection"]
    if "login" not in data_row and "password" not in data_row:
        return Answer("Login and password should be entered", error=True)
    login = data_row["login"]
    password = data_row["password"]
    old_name = collection["old"]
    new_name = collection["new"]
    return system_change.rename_collection(database, old_name, new_name, login, password)


def drop_collection(data_row):
    database = data_row["database"]
    collection = data_row["collection"]
    if "login" not in data_row and "password" not in data_row:
        return Answer("Login and password should be entered", error=True)
    login = data_row["login"]
    password = data_row["password"]
    return system_change.drop_collection(database, collection, login, password)


def create_database(data_row):
    database = data_row["database"]
    if "login" not in data_row and "password" not in data_row:
        return Answer("Login and password should be entered", error=True)
    login = data_row["login"]
    password = data_row["password"]
    return system_change.create_database(database, login, password)


def drop_database(data_row):
    database = data_row["database"]
    if "login" not in data_row and "password" not in data_row:
        return Answer("Login and password should be entered", error=True)
    login = data_row["login"]
    password = data_row["password"]
    return system_change.drop_database(database, login, password)
