def next_greater(arr):
    s = [0]  # list[int]. maintains as a stack the indices of a non-increasing subsequence of a
    ng = [None] * len(arr)  # list[T]. ng[i]: first j in a[i:] s.t. j > a[i], or None if such j does not exist
    for i, x in enumerate(arr[1:], start=1):
        while len(s) > 0 and arr[s[-1]] < x:  # for all elements y in stack s.t. y < x
            ng[s.pop()] = x
        s.append(i)
    return ng

if __name__ == '__main__':
    from random import shuffle
    for _ in range(100):
        a = list(range(10)) * 5
        shuffle(a)
        assert next_greater(a) == [next((x for x in a[i+1:] if x > a[i]), None) for i in range(len(a))]
