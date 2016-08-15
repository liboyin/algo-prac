from math import inf, isfinite, sqrt

def search(n):
    """
    Returns the minimum number of positive integers whose square sum equals the given positive integer.
    Observations:A positive integer is:
        1. a square if and only if each prime factor occurs to an even power in the number's prime factorization.
        2. a sum of two squares if and only if each prime factor that's 3 modulo 4 occurs to an even power in the
            number's prime factorization. ref: https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares
        3. a sum of three squares if and only if it's not of the form 4^a(8b+7) with integers a and b.
            ref: https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem
        4. a sum of four squares. ref: https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem
    Time complexity is O(\sqrt n). Space complexity is O(1).
    :param n: int, positive
    :return: int, in range [1, 4]
    """
    assert n > 0
    while n % 4 == 0:
        n //= 4
    if n % 8 == 7:
        return 4  # ref:
    if round(sqrt(n)) ** 2 == n:  # use round() to eliminate numerical error
        return 1
    a = 1
    while a * a <= n:
        b = round(sqrt(n - a * a))
        if a * a + b * b == n:
            return 1 if b == 0 else 2
        a += 1
    return 3

def search2(n):  # DP. O(n\sqrt n) time, O(n) space
    assert n > 0
    dp = [inf] * (n+1)
    i = 1
    while i * i <= n:
        dp[i*i] = 1
        i += 1
    for i in range(1, n+1):
        if isfinite(dp[i]):
            j = 1
            while i + j * j <= n:
                dp[i+j*j] = min(dp[i+j*j], dp[i]+1)
                j += 1
    return dp[-1]

def search3(n):  # DP with dynamic array. O(n\sqrt n) time, O(n) space
    assert n > 0
    dp = [0]
    while len(dp) <= n:
        dp.append(min(dp[-i*i] for i in range(1, int(sqrt(len(dp))+1))) + 1)  # consider n-1^2, n-2^2, ...
    return dp[n]

if __name__ == '__main__':
    for i in range(1, 100):
        assert search(i) == search2(i) == search3(i)
