def add(x, y):
    if y == 0:
        return x
    return add(x ^ y, (x & y) << 1)

def add2(x, y):
    while y > 0:
        temp = x & y
        x = x ^ y
        y = temp << 1
    return x

if __name__ == '__main__':
    from random import randint
    for _ in range(10000):
        bound = 1 << 30
        x = randint(0, bound)
        y = randint(0, bound)
        assert x + y == add(x, y) == add2(x, y)
