def count1s(n):
    """
    Counts the number of 1s in all positive integers less than or equal to n.
    Observation: Consider count1s(121):
          0   1   2   3   4   5   6   7   8   9
         10  11  12  13  14  15  16  17  18  19
         20  21  22  23  24  25  26  27  28  29
         30  31  32  33  34  35  36  37  38  39
         40  41  42  43  44  45  46  47  48  49
         50  51  52  53  54  55  56  57  58  59
         60  61  62  63  64  65  66  67  68  69
         70  71  72  73  74  75  76  77  78  79
         80  81  82  83  84  85  86  87  88  89
         90  91  92  93  94  95  96  97  98  99
        100 101 102 103 104 105 106 107 108 109
        110 111 112 113 114 115 116 117 118 119
        120 121
    Imagine the collection of numbers as an D-dimensional cube. Consider the number of 1s in each axis. An axis may be
        full (if the digit on that axis is >= 2) or partial (if the digit on that axis is <= 1), or both. In the above
        example, axis 1 (\d*1\d) is full; axis 2 (1\d\d) is partial; axis 0 (\d*1) is both full and partial. In regex
        syntax, consider count(\d*1) + count(\d*1\d) + count(\d*1\d\d) + ...
    Iteration of parameters is shown as follows:
           n |   121 |   12 |     1
           r | +12+1 | +0+2 | +0+22  (+full+partial)
         mag |    10 |  100 |  1000
        tail |     2 |   22 |   122
    Time complexity is O(\sqrt n). Space complexity is O(1).
    :param n: int, positive
    :return: int, positive
    """
    r = 0
    mag = tail = 1  # tail is initialised as 1 since it is a count from 0
    while n > 0:
        r += (n + 8) // 10 * mag  # 32 -> 4: 1, 11, 21, 31; 31 -> 3: 1, 11, 21 (31 itself is handled by the next line)
        if n % 10 == 1:  # consider the last digit
            r += tail
        tail += n % 10 * mag  # last_digit + 1, last_2_digits + 1, ...
        mag *= 10  # magnitude: 1, 10, 100, ...
        n //= 10
    return r

def count_k(n, k):
    assert 0 <= k <= 9
    if k == 0:
        k = 10
    r = 0
    mag = tail = 1
    while n > 0:
        r += (n + (9-k)) // 10 * mag
        if n % 10 == k % 10:
            r += tail
        tail += n % 10 * mag
        mag *= 10
        n //= 10
    return r

def visualise(n):
    assert 0 <= n < 1000
    for i in range(n+1):
        if i % 10 == 9:
            print(i)
        else:
            print(i, end='\t')

if __name__ == '__main__':
    # visualise(121)
    def control(n, k):
        s = ''
        for i in range(1, n+1):  # all positive integers
            s += str(i)
        return s.count(str(k))
    for n in range(1, 1000):
        for k in range(10):
            assert count_k(n, k) == control(n, k)
