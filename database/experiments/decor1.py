from database.experiments.decor import db_function


class Add:
    @db_function("cash")
    def cash(self):
        pass

    @db_function("polip")
    def polip(self):
        pass
