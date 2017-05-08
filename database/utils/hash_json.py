import mmh3

from database.utils.JSON import to_json
from database.utils.base62 import encode


def get_hash(data):
    data = to_json(data)
    hash_code = abs(mmh3.hash(to_json(data)))
    return encode(hash_code)

if __name__ == '__main__':
    a = {"collection": "london", "trigger":{"before_update": "gomer"}}
    print(get_hash(a))