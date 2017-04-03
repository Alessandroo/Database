from database.utils.JSON import from_json, to_json
import os


def LastRow(fileName, MAX_ROW=200):
    """отдать последнюю строку файла"""
    with open(fileName, "rb") as f:
        f.seek(-min(os.path.getsize(fileName), MAX_ROW), 2)
        return (f.read().splitlines())[-1].decode("utf-8")


if __name__ == '__main__':
    fileName = "ex1.json"
    print(LastRow(fileName))
