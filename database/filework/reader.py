from database.parsing.JSON import from_json

if __name__ == '__main__':
    filename = "ex.json"
    list = []
    try:
        with open(filename) as file:
            for line in file.readlines():
                list.append(from_json(line))
    except FileNotFoundError:
        print('File not found')

    print(list)