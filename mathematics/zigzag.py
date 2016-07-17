from itertools import chain
from lib import stated_map
from operator import add

def convert(s, n):
    def coord(x):
        sec, rem = divmod(x, sec_size)
        if rem < n:
            return 2 * sec, rem
        return 2 * sec + 1, sec_size - rem
    m = len(s)
    if n == 0:
        return ''
    if n == 1 or n >= m:
        return s
    if n == 2:
        upper = [s[i] for i in range(0, m, 2)]
        lower = [s[i] for i in range(1, m, 2)]
        return ''.join(chain(upper, lower))
    sec_size = 2 * n - 2
    j_width = [0] * n
    for x in range(max(0, m-sec_size), m):
        i, j  = coord(x)
        j_width[j] = max(j_width[j], i + 1)
    # assert all(x > 0 for x in j_width)
    j_width[0] = j_width[0] // 2 + 1
    j_width[-1] = j_width[-1] // 2 + 1
    sum_before = list(stated_map(add, chain([0], j_width), 0))
    # assert sum_before[-1] == m
    r = [None] * m
    for x in range(m):
        i, j = coord(x)
        if j == 0 or j == n - 1:
            # assert i % 2 == 0
            y = sum_before[j] + i / 2
            r[int(y)] = s[x]
        else:
            y = sum_before[j] + i
            r[int(y)] = s[x]
    # assert not any(x is None for x in r)
    return ''.join(r)

if __name__ == '__main__':
    s = 'PAYPALISHIRING'
    std_test = {1: 'PAYPALISHIRING',
                2: 'PYAIHRNAPLSIIG',
                3: 'PAHNAPLSIIGYIR',
                4: 'PINALSIGYAHRPI',
                5: 'PHASIYIRPLIGAN'}
    for k, v in std_test.items():
        assert convert(s, k) == v
    # n=2:
    # PYAIHRN
    # APLSIIG
    # n=3:
    # P A H N
    # APLSIIG
    # Y I R
    # n=4:
    # P  I  N
    # A LS IG
    # YA HR
    # P  I
    # n=5:
    # P   H
    # A  SI
    # Y I R
    # PL  IG
    # A   N