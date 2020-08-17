from typing import List, Sequence, Set, Tuple


def search(seq: Sequence[int]) -> List[Tuple[int, int, int]]:
    """15. https://leetcode.com/problems/3sum/

    Given an array of integers, are there elements `a, b, c` such that `a + b + c = 0`?

    Find all unique triplets in the array which gives the sum of zero.

    The solution set must not contain duplicate triplets.

    Time complexity is O(n^2). Space complexity is O(n).
    """
    results: List[Tuple[int, int, int]] = []
    N = len(seq)
    if N < 3:
        return []
    xs: List[int] = sorted(seq)
    for i in range(N - 2):
        if i and xs[i] == xs[i - 1]:
            continue
        # find distinct elements x and y in xs[i + 1:] s.t. x + y == -xs[i]
        seen: Set[int] = set()
        for x in xs[i + 1:]:
            y = -xs[i] - x
            if y in seen:
                # implicitly guarantee that tmp[0] <= tmp[1] <= tmp[2]
                tmp = (xs[i], y, x)
                if not results or results[-1] != tmp:
                    results.append(tmp)
            seen.add(x)
    return results


def ref_search(seq: Sequence[int]) -> Set[Tuple[int, int, int]]:
    results: Set[Tuple[int, int, int]] = set()
    N = len(seq)
    if N < 3:
        return results
    for i in range(N - 2):
        for j in range(i + 1, N - 1):
            for k in range(j + 1, N):
                tmp = [seq[i], seq[j], seq[k]]
                if sum(tmp) == 0:
                    tmp.sort()
                    results.add(tuple(tmp))
    return results


def test_search():
    import numpy as np
    for n in range(32):
        seq = np.random.randint(-n, n + 1, n).tolist()
        assert set(search(seq)) == ref_search(seq)
