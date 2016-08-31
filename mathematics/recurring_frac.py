def search(a, b):
    """
    Prints the recurring part of a decimal fraction.
    1/4 = 0.25{0}
    1/6 = 0.1{6}
    1/7 = 0.{142857}
    :param a: int
    :param b: int
    :return: str
    """
    div = ''
    d = dict()  # dict[int,int]: remainder -> index of (rem // b) in div
    rem = a % b  # starts from the first digit after the point
    while rem not in d:  # the loop runs once more if rem == 0
        d[rem] = len(div)  # len(div) increases by exactly 1 each iteration
        rem *= 10
        div += str(rem // b)
        rem %= b
    return '0' if rem == 0 else div[d[rem]:]

if __name__ == '__main__':
    assert search(1, 4) == '0'
    assert search(50, 22) == '27'
    assert search(1, 6) == '6'
    assert search(1, 7) == '142857'
    assert search(1, 17) == '0588235294117647'
