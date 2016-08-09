def search(text):
    s = []
    m_max = 0
    for i, x in enumerate(text):
        if x == '(':
            s.append(i)
        else:
            if len(s) > 0 and text[s[-1]] == '(':
                s.pop()
                if len(s) == 0:  # everything so far has been consumed
                    m_max = max(m_max, i + 1)
                else:
                    m_max = max(m_max, i - s[-1])
            else:
                s.append(i)
    return m_max

if __name__ == '__main__':
    for k, v in {'': 0, '(()': 2, ')()())': 4, '()()': 4, '()(()': 2}.items():
        assert search(k) == v
