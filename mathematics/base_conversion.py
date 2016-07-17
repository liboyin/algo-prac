def convert(arr, old_base, new_base):
    """
    Converts a number, represented as an array of integers in range [0, old_base), to new_base.
    :param arr: list[int]. big-endian
    :param old_base: int, positive
    :param new_base: int, positive
    :return: list[int]. big-endian
    """
    x = sum(y * old_base ** i for i, y in enumerate(reversed(arr)))
    r = []
    while x > 0:
        r.append(x % new_base)
        x //= new_base
    if len(r) == 0:
        return [0]
    return r[::-1]

if __name__ == '__main__':
    d = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
         'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    for x in range(1000):
        a = [int(y) for y in str(x)]
        assert [d[y] for y in bin(x)[2:]] == convert(a, 10, 2)
        assert [d[y] for y in oct(x)[2:]] == convert(a, 10, 8)
        assert [d[y] for y in hex(x)[2:]] == convert(a, 10, 16)
