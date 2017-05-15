class Answer:
    def __init__(self, info, time=None, error=False):
        self.info = info
        self.time = time
        self.error = error
        self._value = None

    @property
    def value(self):
        return self._value


if __name__ == '__main__':
    property_names = [p for p in dir(Answer) if isinstance(getattr(Answer, p), property)]
    print(property_names)
