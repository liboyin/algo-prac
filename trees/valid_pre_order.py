from math import inf

def verify(seq):
    """
    Verifies whether a sequence is a valid pre-order traversal of a binary search tree, assuming unique elements.
    Observation: In a valid pre-order traversal sequence, if node x has a left child, then:
        1. x.left.val appears immediately after x.val in seq; 2. let i = seq.index(x) (note that seq is not necessarily
        indexable). There exists j s.t. seq[i+1:j] < x, and seq[j:] > x. If x has no left child, then j == i + 1.
    The solution is inspired by the next greater element algorithm. Time complexity is O(n). Space complexity is O(n).
    :param seq: seq[num]
    :return: bool
    """
    s = []  # stack of nodes with open right pointers. a subsequence of the path from root to focus
    lb = -inf  # left bound, or last right turn. path is left-skewed after lb
    for x in seq:
        assert lb not in s
        if x < lb:
            return False
        while len(s) > 0 and s[-1] < x:
            lb = s.pop()  # if x is to be inserted as s[-1].right, a discontinuity is created in stack
        s.append(x)
    return True

if __name__ == '__main__':
    from trees.construction import random_bst
    from trees.traversal import fast_pre_order
    std_test = {(2, 4, 3): True, (2, 4, 1): False, (40, 30, 35, 80, 100): True, (40, 30, 35, 20, 80, 100): False}
    for k, v in std_test.items():
        assert verify(k) == v
    fail_test = {(7, 9, 6, 1, 4, 2, 3, 40), (40, 30, 35, 20, 80, 100)}
    for x in fail_test:
        assert not verify(x)
    for size in range(1, 100):
        rnd_test = random_bst(size)
        assert verify(fast_pre_order(rnd_test))
