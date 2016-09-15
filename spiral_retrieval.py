from lib import rev_range

def spiral(mat):
    m = len(mat)
    if m == 0:
        return
    n = len(mat[0])
    offset = 0
    while True:
        if offset > (min(m, n) - 1) // 2:  # 1 -> 0, 2 -> 0, 3 -> 1, 4 -> 1
            return
        for i in range(offset, n - offset):
            yield mat[offset][i]
        for j in range(offset + 1, m - offset):
            yield mat[j][n-1-offset]
        if offset > min(m, n) / 2 - 1:  # 1 -> -0.5, 2 -> 0, 3 -> 0.5, 4 -> 1
            return
        for i in rev_range(offset, n - offset - 1):
            yield mat[m-1-offset][i]
        for j in rev_range(offset + 1, m - offset - 1):
            yield mat[j][offset]
        offset += 1

if __name__ == '__main__':
    for k, v in {((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)):
                 (1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10),
                 ((1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12), (13, 14, 15, 16, 17, 18)):
                 (1, 2, 3, 4, 5, 6, 12, 18, 17, 16, 15, 14, 13, 7, 8, 9, 10, 11),
                 ((2, 5, 8), (4, 0, -1)): (2, 5, 8, -1, 0, 4)}.items():
        assert tuple(spiral(k)) == v
