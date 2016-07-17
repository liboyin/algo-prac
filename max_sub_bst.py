def search(root):  # assumes unique elements
    def q_sub(x):  # Node[T] -> Optional[tuple[T,T,int]]: min, max, size
        global max_size
        if x.left is None:
            if x.right is None:
                return x.val, x.val, 1
            q_right = q_sub(x.right)
            if q_right is None:
                return None
            r_min, r_max, r_size = q_right
            if x.val >= r_min:
                return None
            max_size = max(max_size, r_size + 1)
            return x.val, r_max, r_size + 1
        elif x.right is None:
            q_left = q_sub(x.left)
            if q_left is None:
                return None
            l_min, l_max, l_size = q_left
            if l_max >= x.val:
                return None
            max_size = max(max_size, l_size + 1)
            return l_min, x.val, l_size + 1
        else:
            q_left = q_sub(x.left)
            q_right = q_sub(x.right)
            if q_left is None or q_right is None:
                return None
            l_min, l_max, l_size = q_left
            r_min, r_max, r_size = q_right
            if not l_max < x.val < r_min:
                return None
            size = l_size + r_size + 1
            max_size = max(max_size, size)
            return l_min, r_max, size
    max_size = 1
    q_sub(root)
    return max_size

# TODO: not tested