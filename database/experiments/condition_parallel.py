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


def worker(works):
    tprint("{} worker-timer {}".format(threading.current_thread().getName(), works))


class ServerTask(threading.Thread):
    def __init__(self, count_workers):
        threading.Thread.__init__(self)
        self.count_workers = count_workers

    def run(self):
        works = {}
        event = threading.Event()
        event.set()
        databases = RecDict()
        databases["london"] = Database("london", 5517)
        databases["paris"] = Database("paris", 5518)
        databases["berlin"] = Database("berlin", 5519)

        for i in range(self.count_workers):
            ServerWorker(works, event, databases, "Read london").start()
        ServerWorker(works, event, databases, "Write warsaw 5520").start()
        threading.Timer(5, worker, args=(works,)).start()


class ServerWorker(threading.Thread):
    def __init__(self, works, event, database, instruction):
        threading.Thread.__init__(self)
        self.works = works
        self.event = event
        self.database = database
        self.instruction = instruction

    def run(self):
        for i in range(5):
            # tprint(self.getName())
            # instruction = input("Instruction: ")
            tprint("{} event {}".format(self.getName(), self.event.is_set()))
            tprint("{} {}".format(self.getName(), self.instruction))
            # if not self.condition.acquire(False):
            #     tprint(self.getName())
            #     tprint("Wait")
            #     with self.condition:
            #         self.condition.wait()
            if self.instruction.split()[0] == "Write":
                if not self.event.is_set():
                    self.event.wait()
                self.event.clear()
                tprint("{} worker-before {}".format(self.getName(), self.works))
                while True in self.works.values():
                    self.event.wait(1)
                    tprint("{} worker-in {}".format(self.getName(), self.works))
                tprint("{} worker-after {}".format(self.getName(), self.works))
                tprint(self.getName())
                tprint("Write instruction")
                tprint(str(self.database))
                # with self.condition:
                self.database[self.instruction.split()[1]] = Database(self.instruction.split()[1],
                                                                      self.instruction.split()[2])
                self.event.set()
                break
            else:
                if not self.event.is_set():
                    self.event.wait()
                self.works[self.getName()] = True
                tprint("Read instruction {}".format(self.getName()))
                tprint("Read {} db {}".format(self.getName(), self.database))
                tprint("Read {} db {}".format(self.getName(), self.database[self.instruction.split()[1]].__repr__()))
                tprint("Read {} fact {}".format(self.getName(), factorial(20000)))
                self.works[self.getName()] = False
                # factorial(50)
                # self.condition.notifyAll()


if __name__ == '__main__':
    ServerTask(6).start()
