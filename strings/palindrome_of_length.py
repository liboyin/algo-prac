p = 29  # smaller prime in the hashing polynomial
q = 7919  # larger prime to set the upper bound of hash function

def palindrome_of_len_k(text, k):
    """
    Yields the starting indices of palindromes of length k in text.
    Solution is rolling hash. Expected time complexity is O(n). Space complexity is O(n).
    :param text: str
    :param k: int, positive
    :return: generator[int]
    """
    assert 0 < k <= len(text)
    t = [ord(x) for x in text]
    h = k // 2
    a = [(p ** i) % q for i in range(h)]  # polynomial factors
    lh = sum((x * y) % q for x, y in zip(t[:h], a)) % q  # left hash
    rh = sum((x * y) % q for x, y in zip(t[k-h: k], reversed(a))) % q  # right hash
    for i in range(len(t) - k):
        if lh == rh and t[i: i+h] == t[i+k-h: i+k][::-1]:  # [::-1] cannot be used with range of slice
            yield i
        lh = (lh - t[i]) // p + (a[-1] * t[i+h]) % q
        rh = (rh - a[-1] * t[i+k-h]) * p + t[i+k] % q

if __name__ == '__main__':
    print(next(palindrome_of_len_k('ABABCBAA', 5), None))
