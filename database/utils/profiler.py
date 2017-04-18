import time


class Profiler:
    def __enter__(self):
        self._startTime = time.time()
        self.total_time = 0
        return self

    def __exit__(self, type, value, traceback):
        # print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))
        self.total_time = round(time.time() - self._startTime, 4)
