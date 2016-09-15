class GlobalTemp:
    def __init__(self, **kwargs):
        self.sentinel = object()
        self.old = dict()
        for k, v in kwargs.items():
            if k in globals():
                self.old[k] = globals()[k]
            else:
                self.old[k] = self.sentinel
        self.new = kwargs

    def __enter__(self):
        for k, v in self.new.items():
            globals()[k] = v  # does not work on locals()
        return self

    def __exit__(self, type, v, traceback):
        for k, v in self.old.items():
            if v is self.sentinel:
                del globals()[k]
            else:
                globals()[k] = v

x, y = 0, 1
print('before entry', x, y)
with GlobalTemp(x=2):
    print('in environment', x, y)
print('after exit', x, y)
