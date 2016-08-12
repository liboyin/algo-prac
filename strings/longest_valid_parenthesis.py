def search(text):
    s = []  # stack of unpaired parenthesis (left & right)
    max_match = 0
    for i, x in enumerate(text):
        if x == '(':
            s.append(i)
        else:
            if len(s) > 0 and text[s[-1]] == '(':
                s.pop()
                match = i + 1 if len(s) == 0 else i - s[-1]  # if s is empty, everything have successfully paired up
                max_match = max(max_match, match)
            else:
                s.append(i)
    return max_match

if __name__ == '__main__':
    for k, v in {'': 0, '(()': 2, ')()())': 4, '()()': 4, '()(()': 2}.items():
        assert search(k) == v
