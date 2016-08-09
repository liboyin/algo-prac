import heapq

def merge(*iters):  # len() is not supported on iterators
    h = []
    for i, xs in enumerate(iters):
        ite = iter(xs)
        for x in ite:
            h.append((x, i, ite))  # heapq resolves ties by looking at the next element of tuple. here, index is added
                # as a tie breaker. as a result, the output sequence is stable
            break
    heapq.heapify(h)
    while len(h) > 0:
        x, i, ite = h[0]
        yield x
        for x in ite:  # add tuple back to h, unless empty
            heapq.heapreplace(h, (x, i, ite))  # more efficient than heappop + heappush
            break  # the else clause is not executed if loop exit is triggered by a break
        else:  # only executed when ite is exhausted
            heapq.heappop(h)

if __name__ == '__main__':
    from lib import is_sorted
    from random import randint
    for _ in range(100):
        arr = [[] for _ in range(10)]
        for x in arr:
            for _ in range(randint(0, 5)):
                x.append(randint(0, 10))
            x.sort()
        assert is_sorted(tuple(merge(*arr)))
