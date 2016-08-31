def search(text):
    """
    Given a string consisting of opening and closing parenthesis, find length of the longest parenthesis substring in
        which opening and closing parenthesis match.
    Time complexity is O(n). Space complexity is O(n).
    :param text: str, consisting of only '(' or ')'
    :return: int
    """
    s = []  # stack of unpaired parenthesis (left & right)
    gmax = 0
    for i, x in enumerate(text):
        if x == '(':
            s.append(i)
        else:
            assert x == ')'
            if s and text[s[-1]] == '(':
                s.pop()
                gmax = max(gmax, i + 1 if not s else i - s[-1])  # if s is empty, everything have successfully paired
                    # up. otherwise, the index of the stack top is the starting index
            else:
                s.append(i)
    return gmax

def search2(text):  # TODO: review
    s = []  # stack of indices of unmatched left brackets
    last = None  # Optional[int]. starting index of the current successful match
    gmax = 0
    for i, x in enumerate(text):
        if x == '(':
            if last is None:  # see the else clause
                s.append(i)
            else:  # text[i-1] is a right bracket matched with text[last]
                s.append(last)
                last = None
        else:
            assert x == ')'
            if s:
                left = s.pop()  # match with the last unmatched left bracket
                gmax = max(gmax, i - left + 1)
                last = left
            else:  # if stack is empty, do a hard reset
                last = None
    return gmax

if __name__ == '__main__':
    from lib import rev_range, sliding_window
    from random import choice
    def control(seq):  # O(n^2)
        def is_balanced(sub):
            d = 0
            for x in sub:
                d += 1 if x == '(' else -1
                if d < 0:
                    return False
            return d == 0
        def step(n):
            for xs in sliding_window(seq, n):
                if is_balanced(xs):
                    return True
            return False
        return next((i for i in rev_range(2, len(seq) + 1) if step(i)), 0)
    for k, v in {'': 0, '(()': 2, '()(()': 2, '()()': 4, '((()': 2, ')()())': 4, '()(()))))': 6}.items():
        assert search(k) == search2(k) == v
    for size in [x for x in range(50) for _ in range(x)]:
        a = ''.join(choice(('(', ')')) for _ in range(size))
        assert search(a) == search2(a) == control(a)
