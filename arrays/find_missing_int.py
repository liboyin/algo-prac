from functools import reduce
from operator import xor

def search(arr):
    """
    Given an unsorted array of continuous integers with a missing element, finds the missing integer.
    Solution is inspired by Cuckoo hashing. As a side effect, the array is sorted with a None indicating the missing element.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[int]
    :return: Optional[int]. None if the given array is empty or no element is missing
    """
    n = len(arr)
    if n == 0:
        return None
    m = min(arr)
    for i, x in enumerate(arr):
        arr[i] = x - m  # shift the smallest element to 0, so that each element indicates an index
    arr.append(None)  # at the end of the cuckoo algorithm, None is placed at where the missing element should be, or
        # at arr[-1] if no element is missing
    for i, x in enumerate(arr):
        if x is not None and i != x:
            j, y = i, None  # j: current index; y: value to be assigned. on the first call, y is None. on subsequent
                # (recursive) calls, j == y. note that on each subsequent call, a cell in arr is set to its appropriate
                # value, hence the overall time complexity is O(n)
            while True:
                if arr[j] == y:  # case 1: the pointers forms a loop, and arr[j] is its start. arr[j] should have been
                    # set to None at the beginning, and set to its appropriate value in the previous iteration
                    break
                if arr[j] is None:  # case 2: the pointers forms a chain, and arr[j] is its tail. meanwhile, the head
                    # of this chain should be a None
                    arr[j] = y
                    break
                temp = arr[j]
                arr[j] = y
                j = y = temp
    for i, x in enumerate(arr[:-1]):
        if x is None:
            return i + m
    return None

def search2(arr):
    """
    Boundary case: If the given array is empty or no element is missing, returns 0.
    Solution is inspired by using XOR to find the only non-duplicated element.
    Time complexity is O(n). Space complexity is O(1).
    :param arr: list[int]
    :return: int
    """
    if len(arr) == 0:
        return 0
    acc = reduce(xor, range(min(arr), max(arr)+1), 0)
    return reduce(xor, arr, acc)

if __name__ == '__main__':
    from random import randint, shuffle
    for size in [x for x in range(1, 100) for _ in range(x)]:
        m = randint(-size, size)
        a = list(range(m, m + size + 1))  # +1 for the element to be removed
        i = randint(0, size)
        k = a[i]
        del a[i]
        shuffle(a)
        if i == 0 or i == size:
            assert search2(a) == 0
            assert search(a) is None  # note that search() has side effect on the input array
        else:
            assert search2(a) == k
            assert search(a) == k
