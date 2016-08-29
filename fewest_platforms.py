from itertools import chain
from lib import fst

def search(arr, dep):
    assert len(arr) == len(dep)
    arr = [(x, True) for x in arr]
    dep = [(x, False) for x in dep]
    n = n_max = 0
    for _, x in sorted(chain(arr, dep), key=fst):
        if x:
            n += 1
            n_max = max(n, n_max)
        else:
            n -= 1
    return n_max

if __name__ == '__main__':
    arrivals = [900, 940, 950, 1100, 1500, 1800]
    departures = [910, 1200, 1120, 1130, 1900, 2000]
    assert search(arrivals, departures) == 3
