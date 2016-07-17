def reverse_int(x):
    if x < 0:
        return -reverse_int(-x)
    if 0 <= x < 10:
        return x
    y = 0
    while x > 0:
        y = (y + x % 10) * 10  # tail 0s are handled automatically
        x //= 10
    return y // 10

if __name__ == '__main__':
    from random import randint, choice
    for _ in range(10000):
        rnd_test = randint(-1<<64, 1<<64)
        control = '-' + str(-rnd_test)[::-1] if rnd_test < 0 else str(rnd_test)[::-1]
        assert reverse_int(rnd_test) == int(control)
