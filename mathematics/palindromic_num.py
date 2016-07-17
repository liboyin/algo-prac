from math import floor, log10

def is_palindromic(x):
    if x < 0:  # negative numbers are not palindromic by definition
        return False
    if 0 <= x < 10:
        return True
    left = int(10 ** floor(log10(x)))  # 999 -> 100; 1000 -> 1000
    right = 1
    while left >= right:
        if x // left % 10 != x // right % 10:
            return False
        left //= 10
        right *= 10
    return True

def next_palindromic(x):
    """
    Returns the next greater palindromic number of a given integer.
    Observation:
    Case 0: (-inf, 8]: next positive number
    Case 1: 10 ^ k - 1 -> 10 ^ k + 1. e.g. 999 -> 1001
    Case 2: If x is palindromic, increase the middle digit (odd n) or the last digit of the left half (even n) by 1,
        then copy the left half to the right in reversed order. e.g. 1234 -> 1331
    Case 3. Otherwise, try to copy the left half to the right in reversed order. If the result is smaller than x, follow
        case 2. e.g. 1234 -> 1331
    :param x: int
    :return: int
    """
    def copy_to_right(x):
        for i in range(m):
            x -= x // (10 ** i) % 10 * (10 ** i)
            x += x // (10 ** (n - 1 - i)) % 10 * (10 ** i)
        return x
    if x < 9:  # case 0
        return max(-1, x) + 1
    if floor(log10(x+1)) == log10(x+1):  # case 1
        return x + 2
    n = floor(log10(x)) + 1  # number of digits. 121 -> 3; 1221 -> 4
    m = n // 2
    if is_palindromic(x):  # case 2
        x += 10 ** m
        if x // (10 ** m) % 10 == 0:  # the increase caused a carry-over
            x = copy_to_right(x)
        elif n % 2 == 0:  # no carry-over, even length
            x += 10 ** (m - 1)
        return x  # no carry-over + odd length requires no copying
    y = copy_to_right(x)  # case 3
    if y > x:
        return y
    return copy_to_right(x + 10 ** m)  # increase middle digit, copy to right

if __name__ == '__main__':
    from lib import kth_of_iter, yield_while
    def build_control(size):
        a = [1]
        for i in range(1, size):
            if a[-1] > i:
                a.append(a[-1])
            else:
                xs = yield_while(i + 1, lambda x: not is_palindromic(x), lambda x: x + 1)
                a.append(kth_of_iter(xs, default=i) + 1)
        return a
    for x in range(10000):
        assert (str(x) == str(x)[::-1]) == is_palindromic(x)
    std_test = {999: 1001, 1234: 1331, 1221: 1331, 23545: 23632}
    for k, v in std_test.items():
        assert next_palindromic(k) == v
    control = build_control(10000)
    for x in range(10000):
        if next_palindromic(x) != control[x]:
            print(x)
