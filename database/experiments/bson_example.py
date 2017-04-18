import bson

from database.utils.JSON import to_json
from database.utils.profiler import Profiler


class Ment:
    def __init__(self, name="alex", age=15):
        self.name = name
        self.age = age
        self.language = ["greece", "spanish", "english"]


if __name__ == '__main__':
    print(Ment("lol", 18).__dict__, Ment("alala", 547).__dict__, Ment("helga").__dict__)
    a = to_json(Ment("lol", 18).__dict__)
    b = to_json(Ment("alala", 547).__dict__)
    c = to_json(Ment("helga").__dict__)

    text = [a, b, c]

    print(text)

    a_bson = bson.dumps(Ment("lol", 18).__dict__)
    b_bson = bson.dumps(Ment("alala", 547).__dict__)
    c_bson = bson.dumps(Ment("helga").__dict__)

    text_bson = [a_bson, b_bson, c_bson]

    print(text_bson)

    print("JSON")
    with Profiler():
        with open('ex2.json', 'w+') as file:  # a - дописать w+ писать с начала
            for i in range(int(1e7)):
                for index in text:
                    # print("begin: " + str(file.tell()))
                    file.write(index + '\n')

    print("BSON")
    with Profiler():
        with open('ex2.bson', 'wb') as file:  # a - дописать w+ писать с начала
            for i in range(int(1e7)):
                for index in text_bson:
                    # print("begin: " + str(file.tell()))
                    file.write(index)
                    # file.write('/n')
