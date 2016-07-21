def search(arr):
    """
    Yields the starting and ending indices of all subarrays whose sum is zero.
    :param arr: list[int]
    :return: generator[tuple[int,int]]
    """
    n = len(arr)
    if n == 0:
        return
    appeared = {0: {0}}  # dict[int, set[int]]. sum(seq[:i]) -> i
    sum_up_to = arr[0]
    for i, x in enumerate(arr[1:], start=1):
        if sum_up_to in appeared:
            for y in appeared[sum_up_to]:
                yield y, i  # sum(arr[y, i]) == 0
            appeared[sum_up_to].add(i)
        else:
            appeared[sum_up_to] = {i}
        sum_up_to += x
    if sum_up_to in appeared:
        for y in appeared[sum_up_to]:
            yield y, n

if __name__ == '__main__':
    from random import randint
    def control(arr):
        n = len(arr)
        for i in range(n):
            for j in range(i, n):
                if sum(arr[i: j+1]) == 0:
                    yield i, j + 1
    std_test = {(0,), (4, 6, 3, -9, -5, 1, 3, 0, 2), (4, 2, -3, 1, 6)}
    for arr in std_test:
        assert set(search(arr)) == set(control(arr))
    for size in range(100):
        a = [randint(-size, size) for _ in range(size)]
        assert set(search(a)) == set(control(a))
