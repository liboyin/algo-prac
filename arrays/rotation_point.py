def search(arr):
    """
    Returns the index of the smallest element in a sorted & rotated array of distinct elements.
    Solution is binary search. Time complexity is O(\log n). Space complexity is O(1).
    :param arr: list[T]. distinct and comparable elements
    :return: int
    """
    n = len(arr)
    left, right = 0, n - 1
    while left < right:  # difference 1. it is possible that left == mid, in which case the search will
        # terminate no later than the next iteration. however, mid == right is not possible
        mid = (left + right) // 2
        if arr[left] > arr[mid]:
            right = mid  # difference 2. in this case, mid may point to the rotation point. example: [3, 1, 2]
        elif arr[mid] > arr[right]:
            left = mid + 1
        else:  # difference 3
            assert arr[left] <= arr[mid] < arr[right]  # equality holds when left == mid == right - 1
            break
    return left

if __name__ == '__main__':
    from random import randint
    std_test = {(3, 1, 2): 1,
                (2, 4, 0, 1): 2,
                (0, 1, 2, 3): 0,
                (2, 3, 4, 1): 3,
                (4, 6, -9, -7): 2}
    for k, v in std_test.items():
        assert search(k) == v
    for _ in range(1000):
        a = sorted({randint(-10, 10) for _ in range(10)})
        n = len(a)
        i = randint(0, n)
        a = a[i:] + a[:i]
        assert search(a) == next((i+1 for i in range(n-1) if a[i] > a[i+1]), 0)
