"""A recursive solver for the 8-Queens Problem

https://en.wikipedia.org/wiki/Eight_queens_puzzle
"""

from typing import Generator

import numpy as np
from numpy import ndarray as NDArray

N = 8


def search(mat: NDArray, row: int) -> Generator[NDArray, None, None]:
    assert row >= 0
    if row == N:
        yield mat
    for col in [
        i for i in range(N) if np.all(mat[: row, i] == 0)  # not occupied horizontally
        and np.all(mat.diagonal(i-row) == 0)  # not occupied on the main diagonal
        and np.all(np.fliplr(mat).diagonal(N-1-i-row) == 0)  # not occupied on the opposite diagonal
    ]:
        mat[row, col] = 1
        yield from search(mat, row+1)
        mat[row, col] = 0


if __name__ == '__main__':
    a = np.zeros((N, N), dtype=int)
    for i, x in enumerate(search(a, 0)):
        print(f'{i}\n{x}')
    assert np.all(a == 0)
