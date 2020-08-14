"""Find the next greater element in a sequence."""
from typing import Dict, List, Sequence, TypeVar

T = TypeVar('T')


def next_greater_index(seq: Sequence[T]) -> List[int]:
    """The solution is a non-increasing stack.

    Time complexity is O(n). Space complexity is O(n).

    Examples:
        >>> next_greater_index([0, 2, 3, 1])
        [1, 2, -1, -1]
    """
    # result[i]: smallest j s.t. a[j] > a[i], or -1 if such j does not exist
    result: List[int] = [-1] * len(seq)
    stack: List[int] = [0]  # non-increasing stack of indices
    for i, x in enumerate(seq[1:], start=1):
        while stack and x > seq[stack[-1]]:  # for all indices j in stack s.t. seq[j] < x
            result[stack.pop()] = i
        stack.append(i)
    return result


def next_greater_element(nums1: Sequence[int], nums2: Sequence[int]) -> List[int]:
    """496. https://leetcode.com/problems/next-greater-element-i/

    Given two arrays (without duplicates) `nums1` and `nums2` where `nums1`’s elements are subset of `nums2`.

    Find all the next greater numbers for `nums1`'s elements in the corresponding places of `nums2`.

    All elements are unique.

    Examples:
        >>> next_greater_element([4, 1, 2], [1, 3, 4, 2])
        [-1, 3, -1]
    """
    if not nums1 or not nums2:
        return []
    nge2: Dict[int, int] = {}  # next greater element for each element in nums2
    stack: List[int] = [0]
    for i, x in enumerate(nums2[1:], start=1):
        while stack and x > nums2[stack[-1]]:
            nge2[nums2[stack.pop()]] = x
        stack.append(i)
    return [nge2.get(x, -1) for x in nums1]


def circular_next_greater_element(nums: List[int]) -> List[int]:
    """503. https://leetcode.com/problems/next-greater-element-ii

    Given a circular array (the next element of the last element is the first element of the array),
    return the next greater number for every element.

    Examples:
        >>> circular_next_greater_element([1, 2, 1])
        [2, -1, 2]
    """
    if not nums:
        return []
    N = len(nums)
    nums2: List[int] = nums + nums
    nge2: List[int] = [-1] * (N * 2)
    stack: List[int] = [0]
    for i, x in enumerate(nums2[1:], start=1):
        while stack and x > nums2[stack[-1]]:
            nge2[stack.pop()] = x
        stack.append(i)
    return nge2[:N]


def days2wait(T: List[int]) -> List[int]:
    """739. https://leetcode.com/problems/daily-temperatures/
    
    Given a list of daily temperatures `T`, return a list such that, for each day in the input,
    tells you how many days you would have to wait until a warmer temperature.

    If there is no future day for which this is possible, put 0 instead.

    Examples:
        >>> days2wait([73, 74, 75, 71, 69, 72, 76, 73])
        [1, 1, 4, 2, 1, 1, 0, 0]
    """
    result: List[int] = [0] * len(T)
    stack: List[int] = [0]
    for i, x in enumerate(T[1:], start=1):
        while stack and x > T[stack[-1]]:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result


def ref_next_greater_index(seq: Sequence[T]) -> List[int]:
    """Brute-force reference of next_greater_index()."""
    N = len(seq)
    return [
        next((j for j in range(i + 1, N) if seq[j] > seq[i]), -1)
        for i in range(N)
    ]


def test_next_greater_index():
    from random import shuffle
    assert next_greater_index([]) == []
    for size in [x for x in range(20) for _ in range(x)]:
        seq = list(range(size)) * 3
        shuffle(seq)
        assert next_greater_index(seq) == ref_next_greater_index(seq)
