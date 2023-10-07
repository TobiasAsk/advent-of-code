def move(elem_idx: int, num_moves: int, elements: list):
    i = elem_idx
    for _ in range(abs(num_moves)):

        if i == 0 and num_moves < 0 or i == len(elements)-1 and num_moves > 0:
            elem = elements.pop(i)
            elements.insert(len(elements)-i, elem)

        else:
            next_idx = i+1 if num_moves > 0 else i-1
            elements[i], elements[next_idx] = elements[next_idx], elements[i]

        i += 1 if num_moves > 0 else -1
        i %= len(elements)


a = ['A', 'B', 'C']
move(elem_idx=0, num_moves=5, elements=a)
print(a)
