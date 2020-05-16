from collections import Counter, OrderedDict
from lib import kth_of_iter

def k_divisible_pairs(seq, k):
    # whether seq can be divided into pairs such that the sum of each pair is divisible by k
    if len(seq) & 1:
        return False
    c = Counter(map(lambda x: x % k, seq))
    for x in c.keys():
        if c[x] != c[k - x]:  # if x == k / 2, then c[x] == c[k - x]
            return False
    return True

def kth_unique(seq, k):
    """
    Solution is OrderedDict, which maintains the order in which keys were first inserted.
    Expected time complexity is O(n). Space complexity is O(n).
    :param seq: iterable[T], where T is hashable
    :param k: int. a cardinal number
    :return: Optional[T]. returns None if the required element does not exist
    """
    assert k > 0
    c = OrderedDict()  # implementation of OrderedDict is similar to LRU Cache
    for x in seq:
        c[x] = c.get(x, 0) + 1
    return kth_of_iter((x for x in c.keys() if c[x] == 1), k - 1)

if __name__ == '__main__':
    print(k_divisible_pairs([92, 75, 65, 48, 45, 35], 10))
    print(kth_unique('EABCDFGABHCD', 2))
