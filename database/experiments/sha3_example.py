from Cryptodome.Hash import SHA3_512

if __name__ == '__main__':
    myHash = SHA3_512.new("hello".encode('utf-8')).hexdigest()
    print(SHA3_512.new("hello".encode('utf-8')).hexdigest())