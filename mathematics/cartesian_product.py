from collections import deque

def product(*iters, reverse=False):
    """
    Recursion-free implementation of itertools.product with manually managed stack/queue.
    Time complexity is O(\prod n_i), where n_i is the size of each iterator. Space complexity is O(\prod n_i).
    :param iters: *iterable[T]. As in itertools.product, each iterable must be non-empty, otherwise nothing is generated.
    :param reverse: bool. product(..., reverse=True) is equivalent to product(..., reverse=False) with each iterable
        reversed. A stack is used instead of a queue for this purpose.
    :return: generator[tuple[*T]].
    """
    n = len(iters)
    q = deque()
    q.append(([], 0))  # deque[tuple[list[T],int]]
    while len(q) > 0:
        xs, i = q.pop() if reverse else q.popleft()
        if i == n:
            yield tuple(xs)
        else:
            for y in iters[i]:
                new = list(xs)
                new.append(y)
                q.append((new, i + 1))

if __name__ == '__main__':
    from itertools import product as control
    from lib import iter_equals
    xs = [1, 2], [3, 4, 5], [6, 7, 8, 9]
    assert iter_equals(control(*xs), product(*xs))
    assert iter_equals(list(control(*xs))[::-1], product(*xs, reverse=True))
