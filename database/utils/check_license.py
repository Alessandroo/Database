import binascii
import os

import bson
from ecdsa import BadSignatureError
from ecdsa import SECP256k1
from ecdsa import SigningKey
from ecdsa import VerifyingKey

import database.utils.base62 as base62
from database.filework.file_worker import enter_in_system_directory


def valid_license():
    old_directory = os.getcwd()
    enter_in_system_directory()
    invalid = False
    try:
        with open('license.bs', 'rb') as file:
            try:
                data = bson.loads(file.read())
            except (IndexError, bson.struct.error):
                print("The file with the signature is corrupted")
                os.chdir(old_directory)
                return False
            if 'key' not in data or 'signature' not in data:
                print("The file with the signature is corrupted")
                os.chdir(old_directory)
                return False
            if data['key'] is None or data['key'] == "":
                data['key'] = input("Enter license key: ")
                invalid = True
            while not check_signature(data['key'], data['signature']):
                print("Incorrect entered license key, try again!")
                data['key'] = input("Enter license key: ")
                invalid = True
            if invalid:
                with open('license.bs', 'wb') as file_to_write:
                    file_to_write.write(bson.dumps(data))
            return True
    except FileNotFoundError:
        print("License file not found")
        return False
    finally:
        os.chdir(old_directory)


def check_signature(key, sign):
    try:
        private_key = hex(base62.decode(key))[2:]
    except ValueError:
        print("The key has invalid characters")
        return False
    try:
        private_key = binascii.unhexlify(private_key)
    except binascii.Error:
        print("The key is invalid")
        return False
    try:
        private_key = SigningKey.from_string(private_key, curve=SECP256k1)
    except AssertionError:
        print("The key is invalid")
        return False
    public_key = binascii.hexlify(private_key.get_verifying_key().to_string()).decode('utf-8')
    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
    try:
        return vk.verify(bytes.fromhex(sign), 'database'.encode('utf-8'))
    except BadSignatureError:
        return False


if __name__ == '__main__':
    # data = {"database": "london", "table": "people", "number": 5}
    # hash = abs(mmh3.hash(to_json(data)))
    # print(encode(hash))
    print(valid_license())
