import os

import bson

from Cryptodome.Hash import SHA3_512

from database.filework.file_worker import enter_in_system_directory
from database.utils.answer import Answer
from database.utils.hash_json import get_hash


def create_collection(database, collection, login=None, password=None, system=False):
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
                    return Answer("Error The file with the signature of database {} is corrupted".format(database),
                                  error=True)
                if "name" in data:
                    if system or ("login" in data and "password" in data and data["login"] == login \
                                          and data["password"] == SHA3_512.new(password.encode('utf-8')).hexdigest()):
                        if data["name"] != database:
                            os.chdir(old_directory)
                            return Answer(
                                "Error The file with the signature of database {} is corrupted".format(database),
                                error=True)
                        if not data["collections"]:
                            data["collections"] = {}
                        if collection in data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collection {} of database {} already exist'.format(collection, database),
                                          error=True)
                        else:
                            data["collections"][collection] = {
                                "files": {'0': "{}.bs".format(get_hash({"collection": collection, "files": '0'}))}}
                            with open(data["collections"][collection]["files"]['0'], 'wb'):
                                pass
                    else:
                        os.chdir(old_directory)
                        return Answer('Login or password for database {} are incorrect'.format(database), error=True)
            try:
                data_to_write = bson.dumps(data)
            except (IndexError, bson.struct.error):
                os.chdir(old_directory)
                return Answer("The file with the signature of database {} is corrupted".format(database), error=True)
            with open('system.bs', 'wb') as file_to_write:
                file_to_write.write(data_to_write)
            os.chdir(old_directory)
            return Answer("Operation finished")
    os.chdir(old_directory)
    return Answer("Database {} does not exit or corrupted".format(database), error=True)


def rename_collection(database, old_name, new_name, login=None, password=None, system=False):
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
                    return Answer("Error The file with the signature of database {} is corrupted".format(database),
                                  error=True)
                if "name" in data:
                    if system or ("login" in data and "password" in data and data["login"] == login \
                                          and data["password"] == SHA3_512.new(password.encode('utf-8')).hexdigest()):
                        if data["name"] != database:
                            os.chdir(old_directory)
                            return Answer(
                                "Error The file with the signature of database {} is corrupted".format(database),
                                error=True)
                        if not data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collections in database {} does not exist'.format(database), error=True)
                        if old_name not in data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collection {} of database {} does not exist'.format(old_name, database), error=True)
                        if new_name in data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collection {} of database {} already exist'.format(new_name, database), error=True)
                        if data["collections"][old_name]:
                            for item in ["files", "indexes"]:
                                if item in data["collections"][old_name]:
                                    if data["collections"][old_name][item]:
                                        for field, old_file_name in data["collections"][old_name][item].items():
                                            new_file_name = "{}.bs".format(get_hash({"collection": new_name, item: field}))
                                            try:
                                                os.rename(old_file_name, new_file_name)
                                            except FileNotFoundError:
                                                os.chdir(old_directory)
                                                return Answer(
                                                    'File {} of collection {} of database {} does not exist'.format(old_file_name,
                                                                                                                    old_name,
                                                                                                                    database),
                                                    error=True)
                                            data["collections"][old_name][item][field] = new_file_name
                        data["collections"][new_name] = data["collections"].pop(old_name)
                    else:
                        os.chdir(old_directory)
                        return Answer('Login or password for database {} are incorrect'.format(database), error=True)
            try:
                data_to_write = bson.dumps(data)
            except (IndexError, bson.struct.error):
                os.chdir(old_directory)
                return Answer("The file with the signature of database {} is corrupted".format(database), error=True)
            with open('system.bs', 'wb') as file_to_write:
                file_to_write.write(data_to_write)
            os.chdir(old_directory)
            return Answer("Operation finished")
    os.chdir(old_directory)
    return Answer("Database {} does not exit or corrupted".format(database), error=True)


def drop_collection(database, collection, login=None, password=None, system=False):
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
                    return Answer("Error The file with the signature of database {} is corrupted".format(database),
                                  error=True)
                if "name" in data:
                    if system or ("login" in data and "password" in data and data["login"] == login \
                                          and data["password"] == SHA3_512.new(password.encode('utf-8')).hexdigest()):
                        if data["name"] != database:
                            os.chdir(old_directory)
                            return Answer(
                                "Error The file with the signature of database {} is corrupted".format(database),
                                error=True)
                        if not data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collections in database {} does not exist'.format(database), error=True)
                        if collection not in data["collections"]:
                            os.chdir(old_directory)
                            return Answer('Collection {} of database {} does not exist'.format(collection, database),
                                          error=True)
                        # TODO remove triggers from virtual memory
                        for item in ["files", "indexes"]:
                            if item in data["collections"][collection]:
                                if data["collections"][collection][item]:
                                    for num, file_name in data["collections"][collection][item].items():
                                        try:
                                            os.remove(file_name)
                                        except FileNotFoundError:
                                            pass
                        del data["collections"][collection]
                    else:
                        os.chdir(old_directory)
                        return Answer('Login or password for database {} are incorrect'.format(database), error=True)
            try:
                data_to_write = bson.dumps(data)
            except (IndexError, bson.struct.error):
                os.chdir(old_directory)
                return Answer("The file with the signature of database {} is corrupted".format(database), error=True)
            with open('system.bs', 'wb') as file_to_write:
                file_to_write.write(data_to_write)
            os.chdir(old_directory)
            return Answer("Operation finished")
    os.chdir(old_directory)
    return Answer("Database {} does not exit or corrupted".format(database), error=True)


def create_database(database, login, password):
    old_directory = os.getcwd()
    enter_in_system_directory()
    if not os.path.isdir(database):
        if os.path.exists(database):
            return Answer('{} already exist, but it is not directory'.format(database), error=True)
        else:
            os.makedirs(database)
    os.chdir(database)
    if os.path.isfile("system.bs"):
        with open("system.bs", 'rb') as file:
            try:
                data = bson.loads(file.read())
            except (IndexError, bson.struct.error):
                os.chdir(old_directory)
                return Answer("The file with the signature of database {} is corrupted".format(database), error=True)
            if "name" in data:
                if data["name"] == database:
                    os.chdir(old_directory)
                    return Answer('Database {} already exist'.format(database), error=True)
                else:
                    os.chdir(old_directory)
                    return Answer("The file with the signature of database {} is corrupted".format(database),
                                  error=True)
    data = {"name": database, "collections": {}, "login": login,
            "password": SHA3_512.new(password.encode('utf-8')).hexdigest()}
    with open('system.bs', 'wb') as file_to_write:
        file_to_write.write(bson.dumps(data))
    os.chdir(old_directory)
    return Answer("Operation finished")


def drop_database(database, login, password):
    old_directory = os.getcwd()
    enter_in_system_directory()
    system_directory = os.getcwd()
    if os.path.isdir(database):
        os.chdir(database)
        database_directory = os.getcwd()
        if os.path.isfile("system.bs"):
            with open("system.bs", 'rb') as file:
                try:
                    data = bson.loads(file.read())
                except (IndexError, bson.struct.error):
                    os.chdir(old_directory)
                    return Answer("Error The file with the signature of database {} is corrupted".format(database),
                                  error=True)
                if "name" in data:
                    if "login" in data and "password" in data and data["login"] == login \
                            and data["password"] == SHA3_512.new(password.encode('utf-8')).hexdigest():
                        if data["name"] != database:
                            os.chdir(old_directory)
                            return Answer(
                                "Error The file with the signature of database {} is corrupted".format(database),
                                error=True)
                        os.chdir(old_directory)
                        if data["collections"]:
                            for collection in data["collections"].keys():
                                drop_collection(database, collection, system=True)
                        os.chdir(database_directory)
                    else:
                        os.chdir(old_directory)
                        return Answer('Login or password for database {} are incorrect'.format(database), error=True)
                else:
                    os.chdir(old_directory)
                    return Answer('Directory {} is not exist'.format(database), error=True)
            os.remove("system.bs")
        else:
            os.chdir(old_directory)
            return Answer("The database {} does not exist", error=True)
    else:
        os.chdir(old_directory)
        return Answer("The database {} does not exist", error=True)
    os.chdir(system_directory)
    if len(os.listdir(database)) == 0:
        os.rmdir(database)
    os.chdir(old_directory)
    return Answer("Operation finished")
