def search(arr, gap):
    """
    Given an int array and an integer gap. Repeatedly remove contiguous triples of (x-k, x, x+k).
    Returns the minimum array size after reduction.
    Solution is DP. Time complexity is O(n^2). Space complexity is O(n^2).
    :param arr: list[int]
    :param gap: int
    :return: int, non-negative
    """
    def step(low, high):  # inclusive low & high
        if high - low < 2:
            return high - low + 1
        if (low, high) in cache:
            return cache[low, high]
        min_len = step(low + 1, high)  # arr[low] is not to be removed
        for i in range(low + 1, high):  # remove (low, i, j)
            for j in range(i+1, high+1):
                if arr[i] - arr[low] == arr[j] - arr[i] == gap and step(low+1, i-1) == step(i+1, j-1) == 0:
                    min_len = min(min_len, step(j+1, high))
        cache[low, high] = min_len
        return min_len
    cache = dict()
    return step(0, len(arr) - 1)

if __name__ == '__main__':
    for k, v in {((2, 3, 4, 5, 6, 4), 1): 0,
                 ((2, 3, 4, 7, 6, 4), 1): 2}.items():
        assert search(*k) == v
