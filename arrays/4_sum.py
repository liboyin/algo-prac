from operator import itemgetter as get_item

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
            k = arr[i] + arr[j]
            if target - k in d:
                for x, y in d[target-k]:
                    if i != x and i != y and j != x and j != y:
                        yield tuple(sorted((x, y, i, j)))
            if k in d:
                d[k].append((i, j))
            else:
                d[k] = [(i, j)]

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
    a.sort(key=get_item(2))
    left = 0
    right = len(a) - 1
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
    def control(arr, m):
        n = len(arr)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if arr[i] + arr[j] + arr[k] + arr[l] == m:
                            yield i, j, k, l
    for size in range(4, 50):
        rnd_test = [randint(-size, size) for _ in range(size)]
        target = randint(-size, size)
        pool = set(control(rnd_test, target))
        assert set(search(rnd_test, target)) == pool
        assert set(search2(rnd_test, target)).issubset(pool)
