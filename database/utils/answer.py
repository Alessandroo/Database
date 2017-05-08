class Answer:
    def __init__(self, info, time=None, error=False):
        self._info = info
        self._time = time
        self._error = error

    @property
    def time(self):
        return self._time

    @property
    def info(self):
        return self._info

    @property
    def error(self):
        return self._error
