from typing import Any, Dict


class GlobalTmpVar:
    def __init__(self, **kwargs):
        self.sentinel: object = object()
        self.old: Dict[str, Any] = dict()
        for k, v in kwargs.items():
            if k in globals():
                self.old[k] = globals()[k]
            else:
                self.old[k] = self.sentinel
        self.new: Dict[str, Any] = kwargs

    def __enter__(self):
        for k, v in self.new.items():
            globals()[k] = v
        return self

    def __exit__(self, type, v, traceback):
        for k, v in self.old.items():
            if v is self.sentinel:
                del globals()[k]
            else:
                globals()[k] = v


if __name__ == '__main__':
    x, y = 0, 1
    print('before entry', x, y)
    with GlobalTmpVar(x=2):
        print('in environment', x, y)
    print('after exit', x, y)
