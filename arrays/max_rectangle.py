from lib import rev_range

def search(mat):
    """
    Returns the area of the maximum all-1 rectangle in a given matrix.
    Solution is to find the max rectangle under hist for the submatrix above each row.
    Time complexity is O(n^2). Space complexity is O(n^2).
    :param mat: list[list[bool]]
    :return: int, non-negative
    """
    if len(mat) == 0 or len(mat[0]) == 0:  # numpy compatibility
        return 0
    max_area = 0
    hist = [0] * len(mat[0])
    for row in mat:
        for i, x in enumerate(row):
            hist[i] = hist[i] + 1 if x else 0
        s = []
        for i, x in enumerate(hist + [0]):  # seal right end
            while s and hist[s[-1]] > x:
                h = hist[s.pop()]
                max_area = max(max_area, h * ((i - s[-1] - 1) if s else i))
            s.append(i)
    return max_area

def search2(mat):
    """
    Returns the area of the maximum rectangle whose four corners are all 1s.
    Time complexity is O(n^3). Space complexity is O(1).
    :param mat: list[list[bool]]
    :return: int, non-negative
    """
    if len(mat) == 0 or len(mat[0]) == 0:  # numpy compatibility
        return 0
    m, n = len(mat), len(mat[0])
    max_area = 0
    for top in range(m):
        for bottom in range(top, m):
            left = next((i for i in range(n) if mat[top][i] == mat[bottom][i] == 1), None)
            if left is None:
                continue
            right = next(i for i in rev_range(n) if mat[top][i] == mat[bottom][i] == 1)
            max_area = max(max_area, (right - left + 1) * (bottom - top + 1))
    return max_area

if __name__ == '__main__':
    import numpy as np
    from random import randint
    def control(mat):
        m, n = mat.shape
        max_area = 0
        for i in range(m):
            for j in range(i, m):
                for k in range(n):
                    for l in range(k, n):
                        if np.all(mat[i:j+1, k:l+1]):
                            max_area = max(max_area, (j-i+1)*(l-k+1))
        return max_area
    def control2(mat):
        max_area = 0
        ijs = np.argwhere(mat)
        for i1, j1 in ijs:
            for i2, j2 in ijs:
                if i1 <= i2 and j1 <= j2 and mat[i1,j2] and mat[i2,j1]:  # top-right and bottom-left
                    max_area = max(max_area, (i2-i1+1) * (j2-j1+1))
        return max_area
    a = [[1, 0, 1, 0, 0],
         [1, 0, 1, 1, 1],
         [1, 1, 1, 1, 1],
         [1, 0, 0, 1, 0]]
    assert search(a) == control(np.array(a, dtype=bool)) == 6
    assert search2(a) == control2(np.array(a, dtype=bool)) == 12
    for size in [x for x in range(15) for _ in range(x)]:
        a = np.random.rand(randint(0, size), randint(0, size)) > 0.5
        assert search(a) == control(a)
        assert search2(a) == control2(a), (a, search2(a), control2(a))
