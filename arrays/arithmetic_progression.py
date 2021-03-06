def search(arr):
    """
    Given an arithmetic progression with a missing non-boundary element, returns its insertion point.
    Time complexity is O(\log n). Space complexity is O(1).
    :param arr: list[num]. step size must be positive
    :return: int
    """
    n = len(arr)
    if n <= 2:
        return None
    assert arr[1] - arr[0] > 0
    left, right = 0, n - 1
    gap = (arr[right] - arr[left]) / (right - left + 1)  # this line requires exactly one missing element
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == arr[0] + gap * mid:
            left = mid + 1
        elif arr[mid-1] == arr[0] + gap * (mid-1) and arr[mid] > arr[0] + gap * mid:  # mid-1 passed, mid failed
            return mid
        else:
            right = mid - 1

if __name__ == '__main__':
    from random import randint
    for k, v in {(1, 7, 10, 13, 16, 19, 22): 1,
                (-2, -1, 0, 1, 2, 4): 5,
                (1, 10, 19, 37, 46): 3}.items():
        assert search(k) == v
    for size in [x for x in range(4, 200) for _ in range(x)]:
        a = [randint(0, 10)]
        step = randint(1, 10)
        for _ in range(size - 1):
            a.append(a[-1] + step)
        i = randint(1, size - 2)
        del a[i]
        assert search(a) == i
