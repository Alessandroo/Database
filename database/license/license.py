import binascii
import os

import bson
import ecdsa

from database.utils import base62
from database.filework.file_worker import enter_in_system_directory


class License:
    def __init__(self, message='database'):
        self._private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self._public_key = self._private_key.get_verifying_key()
        self._sign = self._private_key.sign(message.encode('utf-8'))

    @property
    def private_key(self):
        return binascii.hexlify(self._private_key.to_string()).decode('utf-8')

    @property
    def public_key(self):
        return binascii.hexlify(self._public_key.to_string()).decode('utf-8')

    @property
    def sign(self):
        return binascii.hexlify(self._sign).decode('utf-8')

    def write_signature(self):
        old_directory = os.getcwd()
        enter_in_system_directory()
        with open("license.bs", "wb") as file:
            dictionary = {"signature": self.sign, "key": ""}
            file.write(bson.dumps(dictionary))
        os.chdir(old_directory)


if __name__ == '__main__':
    a = License()
    print(a.private_key)
    print(a.public_key)
    print(a.sign)
    a.write_signature()
    print("code")
    string = base62.encode(int(a.private_key, 16))
    print(len(string))
    print(string)
