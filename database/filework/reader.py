from database.parsing.JSON import from_json

if __name__ == '__main__':
    filename = "ex.json"
    list = []
    try:
        with open(filename) as file:
            file.seek(151)
            text = file.readline()
            print(from_json(text))
            # line = file[15]
            # a = file.read
            # print(a)
            # for line in file.readlines():
            #     list.append(from_json(line))
    except FileNotFoundError:
        print('File not found')

    print(list)