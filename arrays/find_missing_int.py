def search(arr):  # TODO: change recursion to iteration
    """
    Given an unsorted array of continuous integers with a missing element, finds the missing element.
    Solution is inspired by Cuckoo hashing. Time complexity is O(n). Space complexity is O(1).
    :param arr: list[int]
    :return: Optional[int]. None if the given array is empty or no element is missing
    """
    def cuckoo(i, x):  # i: current index; x: value to be assigned. on the first call, x is None. on subsequent
        # (recursive) calls, i == x. note that on each subsequent call, a cell in arr is set to its appropriate value,
        # hence the overall time complexity is O(n)
        if arr[i] == x:
            return
        if arr[i] is None:
            arr[i] = x
        else:
            j = arr[i]
            arr[i] = x
            cuckoo(j, j)  # recursive call
    if len(arr) == 0:
        return None
    m = min(arr)
    for i, x in enumerate(arr):
        arr[i] = x - m  # shift the smallest element to 0, so that each element indicates an index
    arr.append(None)  # at the end of the cuckoo algorithm, None is placed at where the missing element should be, or
        # at arr[-1] if no element is missing
    for i in range(len(arr)):
        if arr[i] is not None and arr[i] != i:
            cuckoo(i, None)  # case 1: if the path terminates at a None, the starting point should be assigned None
            # case 2: if the path forms an orbit, the starting point will be revisited with its appropriate value
    for i, x in enumerate(arr[:-1]):
        if x is None:
            return i + m
    return None

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
            assert search(a) is None
        else:
            assert search(a) == k
