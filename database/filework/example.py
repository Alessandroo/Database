from database.parsing.JSON import to_json


class Ment:
    def __init__(self, name="alex", age=15):
        self.name = name
        self.age = age
        self.language = ["greece", "spanish", "english"]

if __name__ == '__main__':
    filename = "ex.json"
    print(Ment("lol", 18).__dict__, Ment("alala", 547).__dict__, Ment("helga").__dict__)
    a = to_json(Ment("lol", 18).__dict__)
    b = to_json(Ment("alala", 547).__dict__)
    c = to_json(Ment("helga").__dict__)

    text = [a, b, c]

    print(text)

    with open(filename, 'w+') as file:
        for index in text:
            file.write('{0}\n'.format(index))