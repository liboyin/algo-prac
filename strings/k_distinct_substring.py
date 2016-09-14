def search_2(text):
    """
    Finds the length of the maximum substring with no more than 2 distinct characters.
    Time complexity is O(n). Space complexity is O(1).
    :param text: string
    :return: int, non-negative
    """
    n = len(text)
    if n <= 2:  # trivial case
        return n
    left = mid = 0  # left: starting index of substring with <= 2 chars. mid: starting index of substring with 1 char
    max_len = 1
    for i in range(1, n):
        assert left <= mid
        if text[i] == text[i-1]:  # repeats the most recent char
            continue
        if mid == 0 or text[i] == text[mid-1]:  # text[mid-1] is the other char in text[left:i]
        # if mid == 0 or (left < mid and s[i] == s[mid-1]):  # second char
            mid = i
        else:  # consider 'aabbaabbcccccccccc'
            max_len = max(max_len, i - left)
            left = mid
            mid = i
    return max(max_len, n - left)

def search_k(text, k):  # expected O(nk) time, O(k) space
    if len(text) <= k:  # trivial case
        return len(text)
    d = {}  # char -> int: ending index of block
    left = max_len = 0
    for i, x in enumerate(text):
        d[x] = i
        if len(d) > k:
            temp = min(d.values())
            del d[text[temp]]
            left = temp + 1  # first index of the next block
        max_len = max(max_len, i - left + 1)
    return max_len

if __name__ == '__main__':
    from random import sample, randint
    from string import ascii_lowercase as alphabet
    def control(text, k):
        m, n = 0, len(text)
        for i in range(n):
            for j in range(i, n):
                sub = text[i:j+1]
                if len(set(sub)) <= k:
                    m = max(m, len(sub))
        return m
    for size in [x for x in range(25) for _ in range(x)]:
        t = ''.join(x * randint(1, 5) for x in sample(alphabet, size))
        assert search_2(t) == control(t, 2)
        k = randint(1, 5)
        assert search_k(t, k) == control(t, k)
