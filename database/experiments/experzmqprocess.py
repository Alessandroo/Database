import sys
import zmq
from  multiprocessing import Process
import time


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


def worker(number):
    context = zmq.Context()
    work_receiver = context.socket(zmq.REP)
    work_receiver.bind("tcp://127.0.0.1:" + str(number))

    # for task_nbr in range(10000000):
    #     message = work_receiver.recv_string()
    #     tprint(str(number) + message)
    #     work_receiver.send_string(str(number) + message)
    # sys.exit(1)
    while True:
        message = work_receiver.recv_string()
        if message == "kill":
            break
        result = str(number) + " " + message
        tprint(result)
        work_receiver.send_string(result)
    work_receiver.close()

def main():
    a = Process(target=worker, args=(5557, ))
    a.start()
    Process(target=worker, args=(5558,)).start()
    Process(target=worker, args=(5559,)).start()
    Process(target=worker, args=(5560,)).start()
    context = zmq.Context()
    ventilator_send = context.socket(zmq.REQ)
    ventilator_send.connect("tcp://127.0.0.1:5557")
    for num in range(100):
        ventilator_send.send_string("{} MESSAGE".format(num))
        tprint(ventilator_send.recv_string())
        if num == 50:
            # ventilator_send.send_string("")
            a.terminate()
            a.join()
            print(a.is_alive())


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    msg_per_sec = 10000000 / duration

    print("Duration: %s" % duration)
    print("Messages Per Second: %s" % msg_per_sec)
