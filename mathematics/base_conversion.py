def convert(arr, old_base, new_base):
    """
    Converts a number, represented as an array of integers in range [0, old_base), to new_base.
    :param arr: list[int], big-endian
    :param old_base: int, positive
    :param new_base: int, positive
    :return: list[int], big-endian
    """
    assert old_base > 0 and new_base > 0
    x_dec = sum(y * old_base ** i for i, y in enumerate(reversed(arr)))  # processed in little-endian
    r = []
    while x_dec > 0:
        r.append(x_dec % new_base)
        x_dec //= new_base
    if len(r) == 0:
        return [0]
    return r[::-1]

if __name__ == '__main__':
    d = dict((str(i), i) for i in range(10))
    d.update({'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15})
    for x in range(1000):
        a = [int(y) for y in str(x)]
        assert [d[y] for y in bin(x)[2:]] == convert(a, 10, 2)
        assert [d[y] for y in oct(x)[2:]] == convert(a, 10, 8)
        assert [d[y] for y in hex(x)[2:]] == convert(a, 10, 16)
