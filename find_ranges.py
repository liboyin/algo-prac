def summary(arr):
    rs = []  # list[list[num]]
    for x in arr:
        if not rs or rs[-1][-1] + 1 < x:  # rs[-1] may have length 1 or 2
            rs.append([])
        rs[-1][1:] = (x,)  # if len(rs[-1]) == 0 or 1, insert x; if len(rs[-1]) == 2, replace rs[-1][1]
    return ['->'.join(map(str, xs)) for xs in rs]  # if len(xs) == 1, generates str(xs[0])

def find_missing(arr, lower, upper):
    n = len(arr)
    r = []
    left = lower
    for i in range(n + 1):
        right = arr[i] if (i < n and arr[i] <= upper) else upper + 1
        if left <= right:
            if left < right:
                r.append(str(left) if left + 1 == right else '{}->{}'.format(left, right - 1))
            left = right + 1
    return r

if __name__ == '__main__':
    assert summary([0, 1, 2, 4, 5, 7]) == ['0->2', '4->5', '7']
    assert find_missing([0, 1, 3, 50, 75], 0, 99) == ['2', '4->49', '51->74', '76->99']
