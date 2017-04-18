from database.application.data_worker import get_db_functions

if __name__ == '__main__':
    dictionary = get_db_functions()
    print(dictionary)