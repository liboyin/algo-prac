from lib import filter_index, rev_enumerate

def char_index(a):
    alphabet = set(a)
    # alphabet = list(sorted(set(a), key=ord))
    return dict(zip(alphabet, range(len(alphabet))))

def bad_char_shift(p, idx):  # O(km) time & space, where k is the size of alphabet
    a = [[i + 1] * len(idx) for i in range(len(p))]  # len(p) * alphabet_size. default is no-occurrence
    # a[i][j]: number of positions that p should be moved forward, if p[i] fails to match alphabet[j]
    # if alphabet[j] has never occurred in p[: i], then a[i][j] = i + 1 (match p[0] with the next char in x)
    # otherwise, denote by x the index of the rightmost occurrence of alphabet[j] in p, a[i][j] = i - x (match alphabet[j] with p[x])
    d = dict()  # for char c with alphabetical index i, the index of the most recent occurrence (left to right) of c in p
    for i, c in enumerate(p):
        for j in range(len(idx)):
            if j in d:
                a[i][j] = i - d[j]
        d[idx[c]] = i
    return a

def match_len(a, s1, s2):
    if s1 == s2:
        return len(a) - s1
    if s1 > s2:
        return match_len(a, s2, s1)
    if s2 >= len(a):
        return 0
    i = 0
    while s2 + i < len(a) and a[s1 + i] == a[s2 + i]:
        i += 1
    return i

def Z(a):  # fundamental process of finding the redundancy structure. linear time
    n = len(a)
    if n == 0:
        return []
    if n == 1:
        return [1]
    z = [0] * n  # z[i]: length of the longest common prefix between a[i:] and a. a[:z[i]] == a[i:i+z[i]]
    z[0] = n  # a[0:] is a itself
    z[1] = match_len(a, 0, 1)  # explicitly calculates z[1]
    l, r = 1, z[1]  # denote a[:r-l+1] by window_A, a[l:r+1] by window_B, window_A == window_B
    # l, r maintains the left and right (inclusive) cursor of window_B, maximising r (minimising l if multiple exists)
    # maximise r is to guarantee linear time. initially, r = 1 + z[1] - 1
    for i in range(2, n):
        if i > r:  # i is beyond window_B
            z[i] = match_len(a, 0, i)
            if z[i] > 1:  # given i >= r, equivalent to: z[i] > 0 and i + z[i] - 1 > r
                l, r = i, i + z[i] - 1
        else:  # l < i <= r, i.e. i in window_B
            j = i - l  # equivalent index of (i in window_B) in window_A
            # denote a[j:j+z[j]] by window_C. window_C == a[:z[j]], but a[j+z[j]] != a[z[j]]
            d = r - i + 1  # distance from i to r (inclusive)
            if z[j] < d:  # window_C strictly in window_A (no equality)
                # a[i:i+z[j]] == window_C == a[:z[j]], a[i+z[j]] == a[j+z[j]] != a[z[j]]
                z[i] = z[j]  # given z[j] < r - i + 1 and r < n, equivalent to: min(z[j], n - i)
                assert i + z[i] - 1 <= r  # in this case, r cannot possibly be increased, hence no update
            else:  # right bound of window_C exceeds window_A, i.e. j < r - l + 1 <= j + z[j]
                # a[i:r+1] == a[j:r-l+1] == a[:r-l+1-j], r - l + 1 - j == d
                z[i] = min(d + match_len(a, d, r + 1), n - i)
                if z[i] > d:  # equivalent to: z[i] > 0 and i + z[i] - 1 > r. not necessarily True due to the limit of n - i
                    l, r = i, i + z[i] - 1  # update of (l, r) is only necessary for partial match
    return z

def good_suffix_shift(p):
    z = Z(p[::-1])
    z.reverse()  # z^-1[i]: length of the longest common suffix between p[:i+1] and p
    n = len(p)
    a = [n] * n  # a[i]: indices that p should be moved forward, given successful match of p[i+1:], but failure at p[i]
    # case A: p[i+1:] is in p[:i+1], and such match is the longest possible
    # denote p[j:j+k] by window_A, p[i+1:] by window_B. maximise j, s.t. window_A == window_B, and p[j-1] != p[i],
    # where k = (n-1)-(i-1)+1 = n-i+1 is the match length. in this case, a[i] = i - (j - 1)
    for i, x in enumerate(z[:-1]):  # z[-1] == n, hence is not useful
        if x > 0:
            a[n - x - 1] = n - 1 - i  # n-1-i == (n-x-1)-(j-x). n-x-1: left of window_B. j-x: left of window_A
    # case B: a proper suffix of p[i+1:] exists at the beginning of p
    cap = n  # since the shift distance a[i] from case A is smaller than n, it caps a[j] for all j < i
    for i, x in rev_enumerate(a[:-1]):  # a[-1] == 1, hence is not useful
        if i - x == -1:
            cap = min(x, cap)
        a[i] = min(x, cap)
    a[-1] = 1
    return a

def search(text, pattern, verbose=False):  # Boyer-Moore algorithm
    assert 0 < len(pattern) <= len(text)
    idx = char_index(pattern)
    bad = bad_char_shift(pattern, idx)
    good = good_suffix_shift(pattern)
    n = len(pattern)
    i = 0  # cursor on t, left to right
    j = n - 1  # cursor on p, right to left
    while i <= len(text) - n:
        if verbose:
            print(text)
            print(' ' * i + pattern)
            print(' ' * (i + j) + '|')
        while j >= 0 and text[i+j] == pattern[j]:
            j -= 1
            if verbose:
                print(' ' * (i + j) + '|')
        if j == -1:
            yield i
            i += 1  # to the next match
        elif text[i+j] in idx:
            i += max(bad[j][idx[text[i+j]]], good[j])
        else:
            i += good[j]
        j = n - 1

def search2(text, pattern):  # Z-algorithm
    assert 0 < len(pattern) <= len(text)
    assert '$' not in text and '$' not in pattern
    z = Z('{}${}'.format(pattern, text))  # '$' guarantees that z[i] <= len(p) for all i > 0
    n = len(pattern)
    return filter_index(lambda x: x == n, z[n+1:])
