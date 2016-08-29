from collections import defaultdict

def search(arr):
    """
    Finds all non-empty subarrays whose sum is zero.
    Observation: 1. sum(arr[i,j+1]) == sum(arr[:j+1]) - sum(arr[:i+1]); 2. sum(arr[:0]) == 0
    Expected time complexity is O(n). Space complexity is O(n).
    :param arr: list[int]
    :return: generator[tuple[int,int]]
    """
    n = len(arr)
    if n == 0:
        return
    d = defaultdict(lambda: set())  # dict[int, set[int]]. sum(arr[:i]) -> {i}
    d[0].add(0)
    s = 0
    for i, x in enumerate(arr):
        s += x
        for j in d[s]:
            yield j, i + 1  # generation is out-of-order due to use of hash table
        d[s].add(i + 1)

if __name__ == '__main__':
    from random import randint
    def control(arr):  # O(n^3)
        n = len(arr)
        for i in range(n):
            for j in range(i, n):
                if sum(arr[i: j+1]) == 0:
                    yield i, j + 1
    for a in {(0,), (4, 6, 3, -9, -5, 1, 3, 0, 2), (4, 2, -3, 1, 6)}:
        assert set(search(a)) == set(control(a))
    for size in range(1, 50):
        for _ in range(size):
            a = [randint(-size, 2 * size) for _ in range(size)]  # 1/3 instances do not have zero-sum subarray
            assert set(search(a)) == set(control(a))  # includes no solution (empty set)
