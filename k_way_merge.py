import heapq

def merge(*iterables):  # len() is not supported on iterators
    h = []
    for i, xs in enumerate(iterables):
        it = iter(xs)
        for x in it:
            h.append((x, i, it))  # heapq resolves ties by looking at the next element of tuple
            # here, index is added as a tie breaker. as a result, the output sequence is stable
            break
    heapq.heapify(h)
    while len(h) > 0:
        x, i, it = h[0]
        yield x
        for x in it:  # add tuple back to h, unless empty
            heapq.heapreplace(h, (x, i, it))  # more efficient than heappop + heappush
            break  # the else clause is not executed if loop exit is triggered by a break
        else:  # only executed when iterator is exhausted
            heapq.heappop(h)

if __name__ == '__main__':
    from lib import is_sorted
    from random import randint
    for _ in range(100):
        arr = [[] for _ in range(10)]
        for x in arr:
            for _ in range(randint(0, 5)):
                x.append(randint(0, 10))
            x.sort()  # stable sort in place (Timsort, hybrid of merge sort and insertion Sort)
        assert is_sorted(list(merge(*arr)))
