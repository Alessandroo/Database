import sys
from database.utils.profiler import Profiler
from database.filework import fileworker


def create(database, table, data):
    print("create")
    print(data)
    fileworker.write(database, table, [data])


def read(database, table, data):
    print("read")
    print(data)


def update(database, table, data):
    print("update")
    print(data)


def delete(database, table, data):
    print("delete")
    print(data)


if __name__ == '__main__':
    list1 = {}
    print("via Dict")
    with Profiler():
        for i in range(int(1e7)):
            list1[i] = 10 * i
    print("get Elem")
    with Profiler():
        print(list1[int(1e6 + 1)])
    list2 = []
    print("via Tuple")
    with Profiler():
        for i in range(int(1e7)):
            list2.append((i, i * 10))
    print("get Elem")
    with Profiler():
        print(list2[list2.index((int(1e6 + 1), int(1e6 + 1)*10))])

    print('size ' + str(sys.getsizeof(list1) / 2 ** 10))
    print('size ' + str(sys.getsizeof(list2) / 2 ** 10))
