import sys
import threading


def factorial(n):
    num = 1
    while n >= 1:
        num *= n
        n -= 1
    return num


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


class RecDict(dict):
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            self[key] = RecDict()
            return self[key]


class Database:
    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __repr__(self):
        return "{}: {}".format(self.name, self.port)


class ServerTask(threading.Thread):
    def __init__(self, count_workers):
        threading.Thread.__init__(self)
        self.count_workers = count_workers

    def run(self):
        lock = threading.RLock()
        databases = RecDict()
        databases["london"] = Database("london", 5517)
        databases["paris"] = Database("paris", 5518)
        databases["berlin"] = Database("berlin", 5519)

        for i in range(self.count_workers):
            ServerWorker(lock, databases, "Read london").start()
            # ServerWorker(condition, databases, "Write warsaw 5520").start()


class ServerWorker(threading.Thread):
    def __init__(self, lock, database, instruction):
        threading.Thread.__init__(self)
        self.lock = lock
        self.database = database
        self.instruction = instruction

    def run(self):

            # tprint(self.getName())
            # instruction = input("Instruction: ")
            tprint("{} {}".format(self.getName(), self.lock.acquire(False)))
            # if not self.condition.acquire(False):
            #     tprint(self.getName())
            #     tprint("Wait")
            #     with self.condition:
            #         self.condition.wait()
            # if self.instruction.split()[0] == "write":
            #     tprint(self.getName())
            #     tprint("Write instruction")
            #     tprint(str(self.database))
            #     with self.condition:
            #         self.database[self.instruction.split()[1]] = Database(self.instruction.split()[1],
            #                                                                  self.instruction.split()[2])
            # else:
            try:
                tprint("Read instruction {}".format(self.getName()))
                tprint("Read {} db {}".format(self.getName(), self.database))
                tprint("Read {} db {}".format(self.getName(), self.database[self.instruction.split()[1]].__repr__()))
            finally:
                if self.lock.acquire(False):
                    self.lock.release()
            # factorial(50)
            # self.condition.notifyAll()


if __name__ == '__main__':
    ServerTask(6).start()
