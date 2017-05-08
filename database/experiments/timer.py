import threading
import time


def delayed():
    print('worker running')
    return


t1 = threading.Timer(3, delayed)
t1.setName('t1')
t2 = threading.Timer(3, delayed)
t2.setName('t2')

print('starting timers')
t1.start()
t2.start()

print('waiting before canceling %s', t2.getName())
time.sleep(2)
print('canceling %s', t2.getName())
t2.cancel()
print('done')
