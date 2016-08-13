import numpy as np

def mul(A, B):  # multiply 2 2*2 matrices
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]))

def fibonacci(n):
    """
    Computes the n_th Fibonacci number.
    idx: 0, 1, 2, 3, 4, 5,  6,  7,  8,  9, ...
    fib: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
    Time complexity is O(\log n). Space complexity is O(\log n).
    :param n: int, non-negative
    :return: int
    """
    assert n >= 0
    a = [(1, np.asarray([[1, 1], [1, 0]], dtype=int))]  # f = [[1, 1], [1, 0]]
    i = 1
    while i < n:
        i <<= 1  # 2, 4, ..., 2 ^ floor(log2(n))
        x = a[-1][1] @ a[-1][1]  # f ^ 2, f ^ 4, ...
        a.append((i, x))
    m = np.asarray([[1, 0], [0, 1]], dtype=int)
    for i, x in reversed(a):
        if i < n:
            m = m @ x
            n -= i
    return m[0].sum()  # equivalent to (m @ np.asarray([1, 1], dtype=int))[0]

def fibonacci2(n):  # tested speed same as non-recursive fibonacci()
    def step(i):
        if i <= 1:
            return np.asarray([[1, 1], [1, 0]], dtype=int)
        m = step(i // 2)  # recursive call
        m2 = m @ m
        if i & 1:
            return m2 @ np.asarray([[1, 1], [1, 0]], dtype=int)
        return m2
    assert n >= 0
    return step(n)[1].sum()  # equivalent to (step(n) @ np.asarray([1, 1], dtype=int))[1]

def last_digit(n):
    a = [1, 1]
    while len(a) < 60:
        a.append((a[-2] + a[-1]) % 10)
    return a[n % 60]

if __name__ == '__main__':
    first_92 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711,
                28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887,
                9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733,
                1134903170, 1836311903, 2971215073, 4807526976, 7778742049, 12586269025, 20365011074, 32951280099,
                53316291173, 86267571272, 139583862445, 225851433717, 365435296162, 591286729879, 956722026041,
                1548008755920, 2504730781961, 4052739537881, 6557470319842, 10610209857723, 17167680177565,
                27777890035288, 44945570212853, 72723460248141, 117669030460994, 190392490709135, 308061521170129,
                498454011879264, 806515533049393, 1304969544928657, 2111485077978050, 3416454622906707,
                5527939700884757, 8944394323791464, 14472334024676221, 23416728348467685, 37889062373143906,
                61305790721611591, 99194853094755497, 160500643816367088, 259695496911122585, 420196140727489673,
                679891637638612258, 1100087778366101931, 1779979416004714189, 2880067194370816120, 4660046610375530309,
                7540113804746346429]  # 64-bit int only holds up to fib(92)
    for i, x in enumerate(first_92):
        fib = fibonacci(i)
        assert fib == x == fibonacci2(i)
        assert fib % 10 == last_digit(i)
