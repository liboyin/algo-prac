from operator import itemgetter as get_item

def search(arr, target):
    """
    Finds all triples of index i, j, k, s.t. arr[i] + arr[j] + arr[k] == target.
    Expected time complexity is O(n^2). Space complexity is O(n^2).
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 3:
        return
    right = dict()  # dict[num,set[int]]: arr[i] -> {i}, where i > mid + 1
    for i, x in enumerate(arr[2:], start=2):
        if x in right:
            right[x].add(i)
        else:
            right[x] = {i}
    for mid in range(1, n-1):  # all indices with a left and a right
        for left in range(mid):
            for i in right.get(target-arr[left]-arr[mid], ()):
                yield left, mid, i  # sequence generation is out-of-order due to the use of set
        x = right[arr[mid+1]]
        x.remove(mid + 1)  # removing an empty entry from dict is not necessary

def search2(arr, target):
    """
    Assuming unique elements, finds all triples of index i, j, k, s.t. arr[i] + arr[j] + arr[k] == target.
    If arr contains repetitions, only a subset of all triples is generated.
    Time complexity is O(n^2). Space complexity is O(n).
    This algorithm can be modified to find arr[i] + arr[j] + arr[k] that approximates target.
    :param arr: list[num]
    :param target: num
    :return: generator[int,int,int], indices in increasing order
    """
    n = len(arr)
    if n < 3:
        return
    a = sorted(enumerate(arr), key=get_item(1))  # sequence generation is out-of-order
    for left in range(n - 1):
        mid = left + 1
        right = n - 1
        while mid < right:  # some have proposed bin_search instead of linear scan. but in case s != target, it would
            # not possible to decide whether left should be increased, or right should be decreased
            ks, xs = zip(*(a[left], a[mid], a[right]))
            s = sum(xs)
            if s == target:
                yield tuple(sorted(ks))
                right -= 1  # repetitions are not handled
            elif s > target:
                right -= 1
            else:
                mid += 1

if __name__ == '__main__':
    from random import randint, shuffle
    def control(arr, m):
        n = len(arr)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if arr[i] + arr[j] + arr[k] == m:
                        yield i, j, k
    for size in range(3, 50):
        rnd_test = [randint(-size, size) for _ in range(size)]
        target = randint(-size, size)
        pool = set(control(rnd_test, target))
        assert pool == set(search(rnd_test, target))
        assert set(search2(rnd_test, target)).issubset(pool)
        rnd_test = list(set(rnd_test))
        shuffle(rnd_test)
        assert set(search(rnd_test, target)) == set(search2(rnd_test, target))
