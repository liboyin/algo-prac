from arrays.max_rectangle_under_hist import search2 as max_rectangle_under_hist
from lib import rev_range

def search(mat):
    """
    Returns the area of the maximum all-1 rectangle in a given matrix.
    Solution is to find the max rectangle under hist for the submatrix above each row.
    Time complexity is O(n^2). Space complexity is O(n^2).
    :param mat: list[list[bool]]
    :return: int, non-negative
    """
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    hists = [[0] * n for _ in range(m)]
    hists[0] = mat[0]
    for i in range(1, m):
        for j in range(n):
            hists[i][j] = hists[i - 1][j] + 1 if mat[i][j] else 0
    return max(max_rectangle_under_hist(x) for x in hists)

def search2(mat):
    """
    Returns the area of the maximum rectangle whose four corners are all 1s.
    Time complexity is O(n^3). Space complexity is O(1).
    :param mat: list[list[bool]]
    :return: int, non-negative
    """
    if not mat or not mat[0]:
        return 0
    m, n = len(mat), len(mat[0])
    max_area = 0
    for top in range(m):
        for bottom in range(top+1, m):
            left = next((i for i in range(n) if mat[top] == mat[bottom] == 1), None)
            if left is None:
                continue
            right = next(i for i in rev_range(n) if mat[top] == mat[bottom] == 1)
            max_area = max(max_area, (right - left + 1) * (bottom - top + 1))
    return max_area

if __name__ == '__main__':
    a = [[1, 0, 1, 0, 0],
         [1, 0, 1, 1, 1],
         [1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0]]
    assert search(a) == 6
    assert search2(a) == 12
