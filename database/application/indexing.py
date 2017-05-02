from database.filework.index_worker import get_indexes, set_indexes
from database.utils.exeptions import IndexNotExist
from database.utils.singleton import SingletonByName


class IndexId(metaclass=SingletonByName):
    def __init__(self, database, table):
        self.database = database
        self.table = table
        try:
            self.__data = get_indexes(database, table)
        except IndexNotExist:
            self.__data = {}

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        set_indexes(self.database, self.table, value)
        self.__data = value
