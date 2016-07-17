from itertools import product
from lib import stated_map

def search(arr):  # Kadane's algorithm
    # key observation:
    # 1. a max-sum subarray must start & finish with a positive number
    # 2. it is safe to discard a subarray with a non-positive sum
    max_sum = max(stated_map(lambda x, s: x + s if x + s > 0 else 0, arr, 0))
    if max_sum > 0:
        return max_sum
    return max(arr)  # if all elements are non-positive

def search2(arr):  # Kadane's algorithm with reconstruction. constant space
    acc, start = 0, 0  # start: pointer to the starting index
    max_range = 0, 0, 0  # range_start, range_end (inclusive), range_acc
    for i, x in enumerate(arr):
        if x + acc <= 0:
            acc = 0
            start = -1
        else:
            acc += x
            if start == -1:
                start = i
            if acc > max_range[2]:
                max_range = start, i, acc
    if max_range[2] > 0:
        return arr[max_range[0]: max_range[1] + 1]
    return [max(arr)]

def search2d(arr, k):  # max sum subarray with size k * k. O(n^2) time & space
    def q(i, j):
        if i < 0 or j < 0:
            return 0
        return a[i][j]
    assert k > 0
    m, n = len(arr), len(arr[0])
    assert m >= k and n >= k
    a = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            a[i][j] = q(i-1, j) + q(i, j-1) - q(i-1, j-1) + arr[i][j]
    for i in range(k-1, m):
        for j in range(k-1, n):
            a[i][j] -= q(i-k, j) + q(i, j-k) - q(i-k, j-k)
    max_i, max_j = max(product(range(k-1, m), range(k-1, n)), key=lambda x: a[x[0]][x[1]])
    return max_i - k + 1, max_j - k + 1, a[max_i][max_j]

if __name__ == '__main__':  # TODO: random test?
    print(search2([-2, -3, 4, -1, -2, 1, 5, -3]))
    m = [[1, 2, -1, 4],
         [-8, -3, 4, 2],
         [3, 8, 10, -8],
         [-4, -1, 1, 7]]
    print(search2d(m, 3))
