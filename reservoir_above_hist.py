from lib import stated_map

def search(hist):
    """
    Returns the total volume reservoir above a given histogram.
    Time complexity is O(n). Space complexity is O(n).
    :param hist: list[int], non-negative
    :return: int, non-negative
    """
    n = len(hist)
    if n < 3:
        return 0
    suffix_max = list(stated_map(max, reversed(hist), hist[-1]))  # max of proper suffix
    del suffix_max[-1]  # equivalent to removing suffix_max[0] after the reverse
    suffix_max.reverse()  # suffix_max[0] will never be accessed. len(suffix_max) == n - 1
    gsum = 0  # global sum of reservoir volume
    m = hist[0]  # inclusive prefix max
    for i in range(1, n-1):  # hist[0] and hist[-1] can never be a valley
        m = max(m, hist[i])
        cap = min(m, suffix_max[i])
        if cap > hist[i]:
            gsum += cap - hist[i]
    return gsum

def visualise(hist):
    m, n = max(hist), len(hist)
    t = [[' '] * n for _ in range(m)]
    for i, x in enumerate(hist):
        for j in range(x):
            t[m - 1 - j][i] = 'x'
    for x in t:
        print(''.join(x))

if __name__ == '__main__':
    for k, v in {(5, 4, 1, 2): 1,
                 (4, 2, 0, 3, 2, 5): 9,
                 (0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1): 6}.items():
        assert search(k) == v
