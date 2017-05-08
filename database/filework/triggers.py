import os

import bson

from database.filework.file_worker import enter_in_system_directory
from database.utils.answer import Answer
from database.filework.system_change import create_collection


def create_unique_trigger(database, collection, field):
    pass


def create_auto_increment_trigger(database, collection, field):
    pass


def create_custom_trigger(database, collection, situation, parameters, code, action=None):
    pass


def create_constraint_trigger(database, collection, field, parent_collection, parent_field):
    pass


def create_check_type_trigger(database, collection, field, types_of_object):
    old_directory = os.getcwd()
    enter_in_system_directory()
    with open("system.bs", 'rb') as file:
        try:
            data = bson.loads(file.read())
        except (IndexError, bson.struct.error):
            os.chdir(old_directory)
            return Answer("Error The file with the signature of database is corrupted", error=True)
        if database in data and os.path.isdir(database):
            if collection in data[database]:
                data[database][collection]["triggers"][field]["check type"] = types_of_object
            # TODO Add to global triggers
            else:
                result = create_collection(database, collection)
                if result.error:
                    return result
                return create_check_type_trigger(database, collection, field, types_of_object)

        else:
            os.chdir(old_directory)
            return Answer("Database {} does not exit or corrupted".format(database), error=True)


def create_not_null_trigger(database, collection, field):
    pass
