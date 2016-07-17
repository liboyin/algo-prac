class PascalTriangle:
    def __init__(self):
        """
        A Pascal triangle is constructed using the recurrent definition of binomial coefficient:
            C(n + 1, k + 1) = C(n, k) + C(n, k + 1)
        The k_th element of the n_th row states the binomial coefficient C(n, k).
        0:									1
        1:								1		1
        2:							1		2		1
        3:						1		3		3		1
        4:					1		4		6		4		1
        5:				1		5		10		10		5		1
        6:			1		6		15		20		15		6		1
        7:		1 		7 		21		35		35		21		7 		1
        8:	1 		8 		28		56		70		56		28		8 		1
        """
        self.a = [[1]]  # base case: n == k == 0

    def query(self, n, k):
        """
        Returns binomial coefficient C(n, k) using Pascal triangle. Note that there are other ways of calculating
            C(n, k), but the Pascal triangle method does not involve any fraction.
        The Pascal triangle is build incrementally. Time complexity is O(n^2). Space complexity is O(n^2).
        :param n: int, non-negative
        :param k: int, non-negative
        :return: int
        """
        assert n >= 0 and k >= 0
        if k > n:
            return 0
        if n == k or k == 0:  # n == k includes n == 0. k == 0 implies n > 0
            return 1
        a = self.a  # shorthand
        if n < len(a):
            return a[n][k]
        for i in range(len(a), n + 1):  # construct an entire row at a time
            r = [1] * (i + 1)
            for j in range(1, i):  # first and last are 1 by definition
                r[j] = a[-1][j-1] + a[-1][j]
            a.append(r)
        return a[n][k]

if __name__ == '__main__':
    def control(n, k):
        if k > n:
            return 0
        if n == k or k == 0:
            return 1
        return control(n-1, k-1) + control(n-1, k)
    pt = PascalTriangle()
    for i in range(10):
        for j in range(10):
            assert pt.query(i, j) == control(i, j)
    catalans = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440, 9694845, 35357670,
                129644790, 477638700, 1767263190, 6564120420, 24466267020, 91482563640, 343059613650, 1289904147324]
    # side note: Wikipedia's second proof (reflection trick) on Catalan number seems most understandable
    for i, x in enumerate(catalans):
        assert x == pt.query(2 * i, i) // (i + 1)
