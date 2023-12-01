import sys
import collections


def move(idx: int, numbers: list):
    num_steps = numbers[idx]
    new_idx = (idx + num_steps) % (len(numbers)-1)

    if num_steps < 0 and new_idx == 0:
        new_idx = len(numbers)-1
    elif num_steps > 0 and new_idx == len(numbers)-1:
        new_idx = 0

    popped = numbers.pop(idx)
    numbers.insert(new_idx, popped)
    return new_idx


def main():
    filename = sys.argv[1]
    with open(filename) as number_list:
        numbers = [int(n)*811589153 for n in number_list]
        # numbers = [int(n) for n in number_list]

    num_mixes, num_moves = 0, 0
    q = collections.deque(range(len(numbers)))

    while num_mixes < 10:
        idx = q.popleft()
        new_idx = move(idx, numbers)
        num_moves += 1

        if new_idx > idx:
            for i in range(len(q)):
                if idx <= q[i] <= new_idx:
                    q[i] -= 1

        elif new_idx < idx:
            for i in range(len(q)):
                if idx >= q[i] >= new_idx:
                    q[i] += 1

        q.append(new_idx)
        num_mixes += num_moves % len(numbers) == 0

    start_idx = numbers.index(0)
    coordinate_sum = sum(numbers[(start_idx+offset) % len(numbers)]
                         for offset in [1000, 2000, 3000])
    print(f'Coordinate sum is {coordinate_sum}')


if __name__ == '__main__':
    main()
