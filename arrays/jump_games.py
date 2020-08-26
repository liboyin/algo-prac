from typing import List, Sequence


def can_reach_tail(seq: Sequence[int]) -> bool:
    """55. https://leetcode.com/problems/jump-game/

    Given an array of non-negative integers, you are initially positioned at the first index of the array.

    Each element in the array represents your maximum jump length at that position.

    Determine if you are able to reach the last index.

    Examples:
        >>> can_reach_tail([2, 3, 1, 1, 4])
        True
        >>> can_reach_tail([3, 2, 1, 0, 4])
        False

    The solution is greedy backtrace. Time complexity is O(n). Space complexity is O(1).
    """
    N = len(seq)
    if N <= 1:
        return True
    furthest = N - 1
    i = N - 1
    while i >= 0:
        if i + seq[i] >= furthest:
            furthest = i
        i -= 1
    return furthest == 0


def can_reach_tail2(seq: Sequence[int]) -> bool:
    """Alternative solution. Time complexity is O(n). Space complexity is O(n)."""
    N = len(seq)
    if N <= 1:
        return True
    mask = [False] * N
    mask[0] = True
    for i in range(N):
        if not mask[i]:
            return False
        x = seq[i]
        if i + x >= N - 1:
            return True
        if mask[i + x]:
            continue
        for j in range(i, i + x + 1):
            mask[j] = True
    return mask[-1]


def test_can_reach_tail():
    from numpy.random import randint
    for n in range(32):
        seq = randint(0, n // 2 + 1, n).tolist()
        assert can_reach_tail(seq) == can_reach_tail2(seq)


def can_reach_zero(seq: List[int], start: int) -> bool:
    """1306. https://leetcode.com/problems/jump-game-iii/

    Given an array of non-negative integers, you are initially positioned at `start` index of the array.
    
    When you are at index `i`, you can jump to `i + arr[i]` or `i - arr[i]`.
    
    Check if you can reach to any index with value 0.

    Notice that you can not jump outside of the array at any time.

    Examples:
        >>> can_reach_zero([4, 2, 3, 0, 3, 1, 2], 5)
        True
        >>> can_reach_zero([4, 2, 3, 0, 3, 1, 2], 0)
        True
        >>> can_reach_zero([3, 0, 2, 1, 2], 2)
        False

    The solution is DFS. This implementation uses explicit stack.

    Time complexity is O(n). Space complexity is O(n).
    """
    N = len(seq)
    if not N:
        return False
    stack: List[int] = [start]
    while stack:
        i = stack.pop()
        x = seq[i]
        if x == -1:
            continue
        if not x:
            return True
        seq[i] = -1
        il = i - x
        if 0 <= il and seq[il] != -1:
            stack.append(il)
        ir = i + x
        if ir < N and seq[ir] != -1:
            stack.append(ir)
    return False


def can_reach_zero2(seq: List[int], start: int) -> bool:
    """Alternative implementation with recursion instead of explicit stack."""
    N = len(seq)
    if not N:
        return False
    def search(i):
        x = seq[i]
        if not x:
            return True
        seq[i] = -1
        results = []
        il = i - x
        if il >= 0 and seq[il] != -1:
            results.append(search(il))
        ir = i + x
        if ir < N and seq[ir] != -1:
            results.append(search(ir))
        return any(results)
    return search(start)


def test_can_reach_zero():
    from numpy.random import randint
    for n in range(1, 32):
        seq = randint(0, n // 2 + 1, n).tolist()
        start = randint(0, n)
        assert can_reach_zero(seq.copy(), start) == can_reach_zero2(seq, start)
