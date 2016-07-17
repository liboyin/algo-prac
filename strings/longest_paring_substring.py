def search(seq):
    """
    Given a string consisting of opening and closing parenthesis, find length of the longest parenthesis substring in
        which opening and closing parenthesis match.
    :param seq: seq[char], where char is either '(' or ')'
    :return: int
    """
    d = c = m = 0  # d: seq[:i+1].count('(') - seq[:i+1].count(')'); c: length of the longest valid parenthesis
    # substring from the last point of reset to seq[i]. m: global maximum of c
    for x in seq:
        if x == '(':  # if there are more opening parenthesis than closing
            d += 1
        elif d == 0:  # if the number of opening and closing parenthesis are equal, and x is a closing parenthesis
            c = 0  # reset d and c
        else:
            d -= 1
            c += 2
            m = max(m, c)
    return m

if __name__ == '__main__':
    std_test = {'((()': 2, ')()())': 4, '()(()))))': 6}
    for k, v in std_test.items():
        assert search(k) == v
