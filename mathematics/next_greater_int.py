from math import floor, log10
from lib import rev_range

def int_to_arr(x):  # big-endian
    assert x >= 0
    n = floor(log10(x)) + 1  # 999 -> 3; 1000 -> 4
    arr = [None] * n
    for i in rev_range(n):
        arr[i] = x % 10
        x //= 10
    assert x == 0
    return arr

def arr_to_int(arr):  # big-endian
    x = 0
    for y in arr:
        assert 0 <= y < 10
        x += y
        x *= 10
    return x // 10

def next_greater_arr(arr):
    n = len(arr)
    pivot = next((i for i in rev_range(n-1) if arr[i] < arr[i+1]), None)
    if pivot is None:
        return None
    min_idx, min_val = pivot+1, arr[pivot+1]  # arr[pivot] < arr[pivot+1] by the definition of pivot
    for i in range(pivot+2, n):  # smallest a[i] s.t. i > pivot and arr[i] > arr[pivot]
        if arr[i] > arr[pivot] and arr[i] < min_val:
            min_idx, min_val = i, arr[i]
    arr[pivot], arr[min_idx] = arr[min_idx], arr[pivot]
    arr[pivot+1:] = sorted(arr[pivot+1:])
    return arr

def next_greater(x):
    if -10 < x < 10:
        return None
    if x < 0:
        x = next_smaller(-x)
        return None if x is None else -x
    a = next_greater_arr(int_to_arr(x))
    return None if a is None else arr_to_int(a)

def next_smaller(x):
    if -10 < x < 10:
        return None
    if x < 0:
        x = next_greater(-x)
        return None if x is None else -x
    a = next_greater_arr([9 - y for y in int_to_arr(x)])
    return None if a is None else arr_to_int(9 - y for y in a)

if __name__ == '__main__':
    from collections import Counter
    def control(x):  # does not handle cases when x does not have a next greater number
        d = Counter(str(x))
        y = x + 1
        while Counter(str(y)) != d:
            y += 1
        return y
    for x in range(100):
        ng = next_greater(x)
        if ng is not None:
            assert ng == control(x)
