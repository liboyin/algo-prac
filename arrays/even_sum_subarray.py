from lib import stated_map
from operator import add

def search(arr):
    """
    Returns the number of subarrays with even sum.
    Observation: 1. sum(arr[i,j+1]) == sum(arr[:j+1]) - sum(arr[:i+1]) 2. sum(arr[:0]) == 0
    Time complexity is O(n). Space complexity is O(1).
    Same logic applies to finding the number of subarrays whose sum is 0, or is divisible by k.
    :param arr: list[int]
    :return: int
    """
    sum_up_to = odd_sum = count = 0  # sum_up_to: sum(arr[:i]). odd_sum: # of j < i where sum(arr[:j]) is odd
    even_sum = 1  # even_sum: # of j < i where sum(arr[:j]) is even. sum([]) == 0, but is not counted
    for x in arr:
        sum_up_to += x
        count += even_sum if sum_up_to % 2 == 0 else odd_sum
        if sum_up_to % 2 == 0:
            even_sum += 1
        else:
            odd_sum += 1
    return count

if __name__ == '__main__':
    from random import randint
    def control(arr):
        n, c = len(arr), 0
        for i in range(n):
            for j in range(i, n):
                if sum(arr[i: j+1]) % 2 == 0:
                    c += 1
        return c
    std_test = {(1, 2, 2, 3, 4, 1): 9}
    for k, v in std_test.items():
        assert search(k) == v
    for size in range(100):
        rnd_test = [randint(0, 100) for _ in range(size)]
        assert search(rnd_test) == control(rnd_test)
