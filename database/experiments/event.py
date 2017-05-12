import threading

import time


def lock_holder(lock, stop_event):
    print('Starting')
    while not stop_event.is_set():
        lock.acquire()
        try:
            print('Holding')
            time.sleep(0.5)
        finally:
            print('Not holding')
            lock.release()
        time.sleep(0.5)
    return


def worker(lock):
    print('Starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        print('Trying to acquire')
        have_it = lock.acquire(False)
        try:
            num_tries += 1
            if have_it:
                print('Iteration %d: Acquired', num_tries)
                num_acquires += 1
            else:
                print('Iteration %d: Not acquired', num_tries)
        finally:
            if have_it:
                lock.release()
        print('Done after %d iterations', num_tries)


lock = threading.Lock()
stop_event = threading.Event()

holder = threading.Thread(target=lock_holder, args=(lock, stop_event), name='LockHolder')
holder.setDaemon(True)
holder.start()

worker = threading.Thread(target=worker, args=(lock,), name='Worker')
worker.start()

worker.join()
stop_event.set()