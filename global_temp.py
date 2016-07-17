class GlobalTemp:
    def __init__(self, **kwargs):
        self.old = dict()
        for k, v in kwargs.items():
            if k in globals():
                self.old[k] = globals()[k]
            else:
                self.old[k] = None
        self.new = kwargs

    def __enter__(self):
        for k, v in self.new.items():
            globals()[k] = v  # does not work on locals()
        return self

    def __exit__(self, type, v, traceback):
        for k, v in self.old.items():
            if v is not None:  # must not abbreviate here. consider v == 0
                globals()[k] = v
            else:
                del globals()[k]
