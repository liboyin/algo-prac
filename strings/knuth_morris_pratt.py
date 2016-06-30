def build_fallback(p):
    assert len(p) > 0
    f = [0, 0]  # f[i]: length of the longest proper prefix in p[0: i] that is also a proper suffix of it
    j = 0  # value of j from one loop is inherited by the next, i.e. j = f[i-1]. crucial for amortised analysis
    for i in range(2, len(p) + 1):  # len(f) == len(p) + 1 when finished, as match length starts from 1
        while j > 0 and p[j] != p[i-1]:
            j = f[j]  # the only chance to decrease. j >= 0 always holds
        if p[j] == p[i-1]:  # the new char matches the next char of prefix
            j += 1  # the only chance to increase j. since j >=0, the amortised complexity is O(n)
            f.append(j)
        else:  # j == 0 and p[0] != p[i-1], i.e. does not match any prefix
            f.append(0)
    return f

def search(text, pattern):
    assert 0 < len(pattern) <= len(text)
    f = build_fallback(pattern)  # len(f) == len(pattern) + 1
    i, j = 0, 0  # i: cursor on pattern; j: cursor on text
    while True:
        if j == len(text):  # end of text
            break
        if text[j] == pattern[i]:  # character match
            i += 1
            j += 1
            if i == len(pattern):
                yield j - i  # yields starting index in text
                i = f[i]  # equivalent to i = f[-1]: a compulsory failure on the next match
        elif i > 0:
            i = f[i]  # fall back, j does not move
        else:  # match fail and fallback exhausted
            j += 1
