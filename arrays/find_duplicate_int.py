from functools import reduce
from operator import xor

def search(arr):
    """
    Given an array containing n+1 integers in range [1, n], finds the duplicated one.
    Observation: Since elements are dense in range [1, n], consider an arbitrary key:
        Case 1: if key < duplicate, then sum(1 for x in arr if x <= key) == key
        Case 2: if key >= duplicate, then sum(1 for x in arr if x <= key) == key + 1
    Time complexity is O(n\log n). Space complexity is O(1).
    :param arr: list[int], positive
    :return: int, positive
    """
    n = len(arr)
    assert n > 0
    left, right = 1, n - 1
    while left <= right:
        mid = (left + right) // 2
        if sum(1 for x in arr if x <= mid) == mid:
            left = mid + 1
        else:
            right = mid - 1
    return left

def search2(arr):
    """
    Observation: Imagine each x in arr is a pointer to arr[x], then the pointers form a \rho structure and possibly
        many loops. And since elements are dense in range [1, n], arr[0] is guaranteed to be the head of the \rho.
        Hence, this problem is equivalent to finding the start of the loop in a linked list, and can be solved with
        Robert Floyd's tortoise and hare algorithm.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[int], positive
    :return: int, positive
    """
    slow = arr[0]
    fast = arr[slow]
    while slow != fast:
        slow = arr[slow]
        fast = arr[arr[fast]]
    slow = 0
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
    return slow

def search3(arr):  # only allows even duplications
    n = len(arr)
    acc = reduce(xor, range(n), 0)
    return reduce(xor, arr, acc)

if __name__ == '__main__':
    from random import choice, shuffle
    for size in [x for x in range(1, 100) for _ in range(x)]:
        a = list(range(1, 1 + size))
        k = choice(a)
        a.append(k)
        shuffle(a)
        assert search(a) == search2(a) == search3(a) == k
