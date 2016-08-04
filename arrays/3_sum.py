from lib import snd

def search(arr, target):
    """
    Finds all triples of index i, j, k, s.t. arr[i] + arr[j] + arr[k] == target.
    Expected time complexity is O(n^2). Space complexity is O(n^2).
    Note that an algorithm that accepts repetitions has a worst case time complexity no lower than O(n^3).
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 3:
        return
    d = dict()  # dict[num,set[int]]: arr[i] -> {i}, where i > mid
    for i, x in enumerate(arr[2:], start=2):
        if x in d:
            d[x].add(i)
        else:
            d[x] = {i}
    for mid in range(1, n-1):  # all indices with a left and a right
        for left in range(mid):
            for i in d.get(target-arr[left]-arr[mid], ()):
                yield left, mid, i  # sequence generation is out-of-order due to the use of set
        x = d[arr[mid+1]]
        x.remove(mid + 1)  # removing an empty entry from dict is not necessary

def search2(arr, target):
    """
    Assuming unique elements, finds all triples of index i, j, k, s.t. arr[i] + arr[j] + arr[k] == target.
    If arr contains repetitions, only a subset of all triples is generated.
    Time complexity is O(n^2). Space complexity is O(n).
    This algorithm can be modified to find arr[i] + arr[j] + arr[k] that approximates the target.
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 3:
        return
    a = sorted(enumerate(arr), key=snd)  # sequence generation is hence out-of-order
    for left in range(n - 1):
        mid = left + 1
        right = n - 1
        while mid < right:  # some have proposed bin_search instead of linear scan. a linear search is able to find
            # the correct index in case of a hit. however, in case of a miss, it would be impossible to decide whether
            # the left or the right cursor should be increased
            js, xs = zip(*(a[left], a[mid], a[right]))  # 'is' is a system keyword
            s = sum(xs)
            if s == target:
                yield tuple(sorted(js))
                right -= 1  # repetitions are not handled
            elif s > target:
                right -= 1
            else:
                mid += 1

if __name__ == '__main__':
    from random import randint, shuffle
    def control(arr, target):  # O(n^3)
        n = len(arr)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if arr[i] + arr[j] + arr[k] == target:
                        yield i, j, k
    for size in range(3, 50):
        a = [randint(-size, size) for _ in range(size)]
        t = randint(-size, size)
        pool = set(control(a, t))
        assert pool == set(search(a, t))
        assert set(search2(a, t)).issubset(pool)
        a = list(set(a))
        shuffle(a)
        assert set(search(a, t)) == set(search2(a, t))
