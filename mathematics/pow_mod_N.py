N = 1337
cache = dict()

def pow_mod_N(a, b):
    """
    Returns a ^ b % N, where b is a large integer represented by a big-endian array.
    Observation: Consider b = 123 = 10^2 * 1 + 10^1 * 2 + 10^0 * 3
    a ^ b = a ^ (10^2 * 1 + 10^1 * 2 + 10^0 * 3)
          = a ^ (10^2 * 1) * a ^ (10^1 * 2) * a ^ (10^0 * 3)
          = a ^ (10^2) ^ 1 * a ^ (10^1) ^ 2 * a ^ (10^0) ^ 3
    :param a: int, positive
    :param b: list[int], non-negative
    :return: int, non-negative
    """
    def step(x, y):
        if y == 0:
            return 1
        if (x, y) in cache:
            return cache[(x, y)]
        h = step(x, y >> 1)
        if y & 1:
            temp = (x * h * h) % N
        else:
            temp = (h * h) % N
        cache[(x, y)] = temp
        return temp
    n = len(b)
    pow_a = [a % N]  # dict[i, ((a % N) ^ (10 ^ i)) % N]
    for _ in range(n-1):
        pow_a.append(step(pow_a[-1], 10))
    acc = 1
    for i, x in enumerate(reversed(b)):
        temp = step(pow_a[i], x)
        acc = acc * temp % N
    return acc

if __name__ == '__main__':
    from mathematics.next_greater_int import int_to_arr
    from random import randint
    for _ in range(1000):
        a, b = randint(1, N), randint(1, N)
        assert pow_mod_N(a, int_to_arr(b)) == a ** b % N
