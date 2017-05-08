import threading
import time

import schedule


def job(t):
    print("I'm working...")
    if t.isAlive():
        print("thread is alive")
    else:
        print("thread don't alive")


def delayed():
    print('worker running')
    return


# schedule.every(10).seconds.do(job)
# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("21:44").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Timer(5, delayed)
    t1.setName('t1')
    t1.start()
    schedule.every(2).seconds.do(job, t1)
    while True:
        schedule.run_pending()
    # schedule.every(2).seconds.do(job, t1)
