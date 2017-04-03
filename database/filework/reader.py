import os

from database.utils.JSON import from_json


if __name__ == '__main__':
    filename = "ex.json"
    list = []
    try:
        with open(filename) as file:
            while not file.tell() == os.fstat(file.fileno()).st_size:
                print("begin: " + str(file.tell()))
                string = file.readline()
                print(string)
                print(len(string))
                print("end: " + str(file.tell()))
            # file.seek(151)
            # text = file.readline()
            # print(from_json(text))
            # line = file[15]
            # a = file.read
            # print(a)
            # for line in file.readlines():
            #     list.append(from_json(line))
    except FileNotFoundError:
        print('File not found')

    print(list)