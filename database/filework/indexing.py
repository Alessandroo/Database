import os
import pickle

import bson

from database.filework.file_worker import read_db_file, enter_in_system_directory
from database.utils.answer import Answer
from database.utils.exceptions import DatabaseNotExist
from database.utils.hash_json import get_hash


def create_btree_index(database, collection, field, data=None, object_types=(bool, int, float)):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    files = data["collections"][collection]["files"]
    files = files.values()
    index_dict = {}
    old_directory = os.getcwd()
    enter_in_system_directory()
    os.chdir(database)
    for file in files:
        with open(file, "rb") as file_data:
            for line in file_data:
                item = bson.loads(line)
                if field in item:
                    if isinstance(item[field], object_types):
                        if item[field] not in index_dict:
                            index_dict[item[field]] = []
                        index_dict[item[field]].append(item["_id"])
    if "indexes" not in data["collections"][collection]:
        data["collections"][collection]["indexes"] = {}
    if field in data["collections"][collection]["indexes"]:
        try:
            os.remove(data["collections"][collection]["indexes"][field]["filename"])
        except FileNotFoundError:
            pass
        del data["collections"][collection]["indexes"][field]
    data["collections"][collection]["indexes"][field] = {"type indexing": "btree", "filename": "{}.bs".format(
        get_hash({"collection": collection, "index": field}))}
    filename = data["collections"][collection]["indexes"][field]["filename"]
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol=0)
    os.chdir(old_directory)
    return Answer("Operation finished")


def create_unique_index(database, collection, field, data=None,
                        object_types=("object", "string", "float", "int", "array", "bool")):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    files = data["collections"][collection]["files"]
    files = files.values()
    index_dict = {}
    old_directory = os.getcwd()
    enter_in_system_directory()
    os.chdir(database)
    for file in files:
        with open(file, "rb") as file_data:
            for line in file_data:
                item = bson.loads(line)
                if field in item:
                    if isinstance(item[field], object_types):
                        if item[field] in index_dict:
                            os.chdir(old_directory)
                            return Answer(
                                "Fields {} in collection {} of {} is not unique".format(field, collection, database),
                                error=True)
                        index_dict[item[field]] = item["_id"]
    if "indexes" not in data["collections"][collection]:
        data["collections"][collection]["indexes"] = {}
    if field in data["collections"][collection]["indexes"]:
        try:
            os.remove(data["collections"][collection]["indexes"][field]["filename"])
        except FileNotFoundError:
            pass
        del data["collections"][collection]["indexes"][field]
    data["collections"][collection]["indexes"][field] = {"type indexing": "unique", "filename": "{}.bs".format(
        get_hash({"collection": collection, "index": field}))}
    filename = data["collections"][collection]["indexes"][field]["filename"]
    with open(filename, 'wb') as file:
        pickle.dump(data, file, protocol=0)
    os.chdir(old_directory)
    return Answer("Operation finished")


def delete_index(database, collection, field, data=None):
    if not data:
        try:
            data = read_db_file(database)
        except DatabaseNotExist as e:
            return Answer(e.__str__(), error=True)
    old_directory = os.getcwd()
    enter_in_system_directory()
    os.chdir(database)
    if "indexes" in data["collections"][collection]:
        if data["collections"][collection]["indexes"] and field in data["collections"][collection]["indexes"]:
            try:
                os.remove(data["collections"][collection]["indexes"][field]["filename"])
            except FileNotFoundError:
                pass
            del data["collections"][collection]["indexes"][field]
    os.chdir(old_directory)
    return Answer("Operation finished")
