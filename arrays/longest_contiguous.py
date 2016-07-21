def subarray(arr):
    """
    A contiguous subarray of an int array contains all integers from min(sub) to max(sub), inclusive.
    Returns the starting and ending (exclusive) index of the longest contiguous subarray.
    Expected time complexity is O(n^2). Space complexity is O(n).
    :param arr: list[int]. must not be empty
    :return: tuple[int, int]
    """
    n = len(arr)
    assert n > 0
    left, right = -1, -1
    for i in range(n):
        s = {arr[i]}
        s_min = s_max = arr[i]
        j = i + 1
        while j < n and arr[j] not in s:  # a contiguous subarray cannot contain duplicates
            s.add(arr[j])
            s_min = min(arr[j], s_min)
            s_max = max(arr[j], s_max)
            if s_max - s_min == j - i and j - i > right - left:
                left, right = i, j
            j += 1
    return left, right

def subsequence(arr):
    """
    A contiguous subsequence of an int array contains all integers from min(sub) to max(sub), inclusive.
    Returns the length of the longest contiguous subsequence.
    Expected time complexity is O(n). Space complexity is O(n).
    :param arr: list[int]
    :return: int
    """
    def reach(x):
        if x - 1 in s:
            return -1
        i = 1
        while x + i in arr:
            i += 1
        return i
    if len(arr) == 0:
        return 0
    s = set(arr)
    return max(map(reach, arr))

def subsequence2(arr):  # not as elegant, but same time complexity
    d = dict()  # dict[int, tuple[int, int]]. x -> min & max element of the longest range containing x
    for x in arr:
        # note that in all 4 cases, only edges of a range needs update, hence faster than union-find
        if x - 1 in d:
            left = d[x-1][0]
            if x + 1 in d:  # case 1: x joins two ranges
                right = d[x+1][1]
                d[left] = d[right] = left, right
            else:  # case 2: x is the new right
                d[left] = d[x] = left, x
        elif x + 1 in d:  # case 3: x is the new left
            right = d[x+1][1]
            d[x] = d[right] = x, right
        else:  # case 4: x is a new range by itself
            d[x] = x, x
    return max(right - left + 1 for left, right in d.values())

if __name__ == '__main__':  # TODO: random test?
    print(subsequence2([36, 41, 56, 35, 44, 33, 34, 92, 43, 32, 42]))
