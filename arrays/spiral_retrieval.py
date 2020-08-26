"""
Given a matrix of `m x n` elements (`m` rows, `n` columns), return all elements of the matrix in spiral order.

54. https://leetcode.com/problems/spiral-matrix/
"""
from typing import Generator, List, Sequence, Tuple, TypeVar

from lib import rev_range

T = TypeVar('T')


def spiral(mat: Sequence[Sequence[T]]) -> Generator[T, None, None]:
    M = len(mat)
    if M == 0:
        return
    N = len(mat[0])
    offset = 0
    while True:
        if offset > (min(M, N) - 1) // 2:  # 1 -> 0, 2 -> 0, 3 -> 1, 4 -> 1
            return
        for i in range(offset, N - offset):
            yield mat[offset][i]
        for j in range(offset + 1, M - offset):
            yield mat[j][N - 1 - offset]
        if offset > min(M, N) / 2 - 1:  # 1 -> -0.5, 2 -> 0, 3 -> 0.5, 4 -> 1
            return
        for i in rev_range(offset, N - offset - 1):
            yield mat[M-1-offset][i]
        for j in rev_range(offset + 1, M - offset - 1):
            yield mat[j][offset]
        offset += 1


def rotate_clockwise(mat: Sequence[Sequence[T]]) -> List[Tuple[T, ...]]:
    """Rotate a matrix clockwise by 90 degrees.

        1 2 3    1 4 7    7 4 1
        4 5 6 -> 2 5 8 -> 8 5 2
        7 8 9    3 6 9    9 6 3
    """
    return list(xs[::-1] for xs in zip(*mat))


def rotate_counter_clockwise(mat: Sequence[Sequence[T]]) -> List[Tuple[T, ...]]:
    """Rotate a matrix counter-clockwise by 90 degrees.

        1 2 3    1 4 7    3 6 9
        4 5 6 -> 2 5 8 -> 2 5 8
        7 8 9    3 6 9    1 4 7
    """
    return list(zip(*mat))[::-1]


def spiral2(mat: Sequence[Sequence[T]]) -> Generator[T, None, None]:
    if not mat:
        return
    yield from mat[0]
    yield from spiral2(rotate_counter_clockwise(mat[1:]))


def test_spiral():
    from numpy.random import randint
    for mat, seq in [
        (
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
            [1, 2, 3, 6, 9, 8, 7, 4, 5]
        ),
        (
            [
                [ 1,  2,  3,  4],
                [ 5,  6,  7,  8],
                [ 9, 10, 11, 12],
                [13, 14, 15, 16],
            ],
            [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
        ),
        (
            [
                [ 1,  2,  3,  4,  5,  6],
                [ 7,  8,  9, 10, 11, 12],
                [13, 14, 15, 16, 17, 18],
            ],
            [1, 2, 3, 4, 5, 6, 12, 18, 17, 16, 15, 14, 13, 7, 8, 9, 10, 11]
        ),
        (
            [
                [2, 5,  8],
                [4, 0, -1],
            ],
            [2, 5, 8, -1, 0, 4]
        ),
    ]:
        assert list(spiral(mat)) == list(spiral2(mat)) == seq
    for _ in range(20):
        shape = randint(1, 6, 2)
        mat = np.arange(shape[0] * shape[1]).reshape(shape).tolist()
        assert list(spiral(mat)) == list(spiral2(mat))
