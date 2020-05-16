from lib import filter3, partition, safe_index
from math import inf

def median_of_two(xs, ys):
    """
    Returns the true median of the merge of two sorted arrays. Let arr = sorted(xs + ys), n = len(arr):
    If n is odd, returns arr[n//2]; otherwise, returns (arr[n/2-1] + arr[n/2]) / 2.
    Expected time complexity is O(\log(m+n)). Space complexity is O(\log(m+n)).
    :param xs: list[num]. sorted
    :param ys: list[num]. sorted
    :return: num
    """
    n = len(xs) + len(ys)
    assert n > 0
    right_median = kth_of_two(xs, ys, n // 2 + 1)  # k starts from 1
    if n & 1:
        return right_median
    left_median = kth_of_two(xs, ys, n // 2)
    return (left_median + right_median) / 2

def kth_of_two(xs, ys, k):
    """
    Returns the k_th smallest element in the merge of two sorted arrays.
    Expected time complexity is O(\log n). Space complexity is O(\log n).
    :param xs: list[num]. sorted
    :param ys: list[num]. sorted
    :param k: int, cardinal
    :return: num
    """
    assert 0 < k <= len(xs) + len(ys)
    if len(xs) == 0:
        return ys[k - 1]
    if len(ys) == 0:
        return xs[k - 1]
    if k == 1:
        return min(xs[0], ys[0])
    h = k // 2  # h is also cardinal
    if safe_index(xs, h-1, inf) < safe_index(ys, h-1, inf):
        return kth_of_two(xs[h:], ys, k - h)  # recursive call
    return kth_of_two(xs, ys[h:], k - h)  # recursive call

def kth(arr, k):
    """
    Returns the k_th smallest element in an unsorted array.
    Expected time complexity is O(\log n). Space complexity is O(\log n).
    :param arr: list[T], where T is comparable
    :param k: int, cardinal
    :return: T
    """
    assert 0 < k <= len(arr)
    lt, eq, gt = filter3(arr, arr[len(arr)//2])
    if k <= len(lt):
        return kth(lt, k)  # recursive call
    elif k > len(lt) + len(eq):
        return kth(gt, k - len(lt) - len(eq))  # recursive call
    else:  # 0 < k - len(lt) <= len(eq)
        return eq[k - 1 - len(lt)]  # order is stable

def kth2(arr, k):
    assert 0 < k <= len(arr)
    i, j = partition(arr, arr[len(arr)//2])[1:]  # arr[:i] < pivot; arr[i:j] == pivot; arr[j:] > pivot
    if k <= i:
        return kth2(arr[:i], k)  # recursive call
    elif k > j:
        return kth2(arr[j:], k - j)
    else:
        return arr[k-1]

if __name__ == '__main__':
    from random import randint
    # test median_of_two and kth_of_two
    for size in range(100):
        left = sorted(randint(-size, size) for _ in range(size))
        right = sorted(randint(-size, size) for _ in range(size+1))
        merge = sorted(left + right)
        for i, x in enumerate(merge):
            assert kth_of_two(left, right, i + 1) == x
        if len(merge) & 1:
            assert median_of_two(left, right) == merge[len(merge)//2]
        else:
            assert median_of_two(left, right) == (merge[len(merge)/2-1] + merge[len(merge)/2]) / 2
    # test kth
    for size in [x for x in range(50) for _ in range(x)]:
        a = [randint(-size, size) for _ in range(size)]
        for i, x in enumerate(sorted(a)):
            assert kth(a, i+1) == kth2(list(a), i+1) == x
