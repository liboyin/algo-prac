import sys

eps = sys.float_info.epsilon

def newton_raphson(f, fp):  # requires fp to be continuous. worst case O(\log n) time
    x = 1
    for _ in range(100):
        yp = fp(x)
        if abs(yp) < eps:
            x += 100 * eps
            continue
        d = f(x) / yp
        if abs(d) < eps:
            return x
        x -= d
    return None  # did not converge

def sqrt(y):
    assert y >= 0
    f = lambda x: x ** 2 - y
    fp = lambda x: 2 * x
    return newton_raphson(f, fp)

def sqrt2(y):  # f(x) = x ^ 2 - y -> x' = (y / x + x) / 2
    assert y >= 0
    x = y / 2
    while True:
        x1 = (y / x + x) / 2
        if abs(x - x1) < eps:
            return x
        x = x1
