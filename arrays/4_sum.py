from operator import itemgetter

def search(arr, target):
    """
    Finds all 4-tuples of index i, j, k, l, s.t. arr[i] + arr[j] + arr[k] + arr[l] == target.
    Expected time complexity is O(n^2). Space complexity is O(n^2).
    Note that an algorithm that accepts repetitions has a worst case time complexity no lower than O(n^4).
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 4:
        return
    d = dict()
    for i in range(n):
        for j in range(i+1, n):
            s = arr[i] + arr[j]
            for x, y in d.get(target-s, ()):
                if i != x and i != y and j != x and j != y:
                    yield tuple(sorted((x, y, i, j)))
            if s in d:
                d[s].append((i, j))
            else:
                d[s] = [(i, j)]

def search2(arr, target):
    """
    Finds a subset of all 4-tuples of index i, j, k, l, s.t. arr[i] + arr[j] + arr[k] + arr[l] == target.
    There is no guarantee on which subset is generated, even when all elements are unique.
    Time complexity is O(n^2\log n). Space complexity is O(n^2).
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 4:
        return
    a = []
    for i in range(n):
        for j in range(i+1, n):
            a.append((i, j, arr[i] + arr[j]))
    a.sort(key=itemgetter(2))  # sort on the sum of pairs. this makes the algorithm highly incompatible to repetitions
    left, right = 0, len(a) - 1
    while left < right:
        il, jl, xl = a[left]
        ir, jr, xr = a[right]
        if xl + xr == target:
            if il != ir and il != jr and jl != ir and jl != jr:
                yield tuple(sorted((il, jl, ir, jr)))
            right -= 1
        elif xl + xr > target:
            right -= 1
        else:
            left += 1

if __name__ == '__main__':
    from random import randint
    def control(arr, target):  # O(n^4)
        n = len(arr)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if arr[i] + arr[j] + arr[k] + arr[l] == target:
                            yield i, j, k, l
    for size in range(4, 50):
        a = [randint(-size, size) for _ in range(size)]
        t = randint(-size, size)
        pool = set(control(a, t))
        assert set(search(a, t)) == pool
        assert set(search2(a, t)).issubset(pool)
