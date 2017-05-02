from database.utils.function_mapper import db_function


class SystemChange:
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
    def create_database():
        pass

    @db_function("dropDataBase", "system")
    def drop_database():
        pass