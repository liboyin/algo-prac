def search_min(arr):
    """
    Returns the index of the smallest element in a sorted & rotated array of distinct elements.
    Solution is binary search. Time complexity is O(\log n). Space complexity is O(1).
    :param arr: list[T]. distinct and comparable elements
    :return: int
    """
    n = len(arr)
    assert n > 0
    left, right = 0, n - 1
    while left < right:  # difference 1. it is possible that left == mid, in which case the search will
        # terminate no later than the next iteration. however, mid == right is not possible
        mid = (left + right) // 2
        if arr[left] > arr[mid]:  # rotation point is in arr[left:mid+1]
            right = mid  # difference 2. in this case, mid may point to the rotation point. example: [3, 1, 2]
        elif arr[mid] > arr[right]:  # rotation point is in arr[mid+1:right+1]
            left = mid + 1
        else:  # difference 3
            # assert arr[left] <= arr[mid] < arr[right]  # equality holds when left == mid == right - 1
            break
    return left

def index(arr, x):
    """
    Returns the index of x in a sorted & rotated array of distinct elements. Returns None if x is not in arr.
    :param arr: list[T]. distinct and comparable elements
    :param x: T
    :return: Optional[int]
    """
    n = len(arr)
    if n == 0:
        return None
    left, right = 0, n - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == x:
            return mid
        if x < arr[mid]:
            if arr[left] <= arr[mid]:  # left is monotonously increasing. equality holds when left == mid
                if arr[left] <= x:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # right is monotonously increasing
                right = mid - 1
        else:
            if arr[mid] < arr[right]:  # right is monotonously increasing. equality only holds when left == right and
                # arr[mid] == x, which has failed already
                if x <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
            else:  # left is monotonously increasing
                left = mid + 1
    return None

if __name__ == '__main__':
    from lib import unique_randints
    from random import randint
    for k, v in {(3, 1, 2): 1,
                (2, 4, 0, 1): 2,
                (0, 1, 2, 3): 0,
                (2, 3, 4, 1): 3,
                (4, 6, -9, -7): 2}.items():
        assert search_min(k) == v
        for i, x in enumerate(k):
            assert index(k, x) == i
    for size in range(1, 1000):
        a = unique_randints(-size, size, size)
        n = len(a)
        i = randint(0, size-1)
        a = a[i:] + a[:i]
        assert search_min(a) == next((i + 1 for i in range(n - 1) if a[i] > a[i + 1]), 0)
        for j, x in enumerate(a):
            assert index(a, x) == j
