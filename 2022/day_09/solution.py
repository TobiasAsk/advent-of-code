DIRECTIONS = {
    'R': (1, 0),
    'U': (0, 1),
    'L': (-1, 0),
    'D': (0, -1)
}


def part1():
    tail_position = head_position = (0, 0)
    tail_positions = {tail_position}

    with open('dag 9/input.txt') as motions:
        for motion in motions:
            parts = motion.split()
            direction, num_steps = DIRECTIONS[parts[0]], int(parts[1])
            delta_x, delta_y = direction

            for _ in range(num_steps):
                head_position = (
                    head_position[0] + delta_x, head_position[1] + delta_y)

                head_x, head_y = head_position
                tail_x, tail_y = tail_position
                delta_tail_x = delta_tail_y = 0

                if abs(head_x - tail_x) == 2 or abs(head_y - tail_y) == 2:
                    delta_tail_x = 1 if head_x > tail_x else -1 if head_x < tail_x else 0
                    delta_tail_y = 1 if head_y > tail_y else -1 if head_y < tail_y else 0

                tail_position = (tail_x + delta_tail_x, tail_y + delta_tail_y)
                tail_positions.add(tail_position)

            # print(f'Head is at ({head_position[0]}, {head_position[1]})')
            # print(f'Tail is at ({tail_position[0]}, {tail_position[1]})')

    print(f'Num positions {len(tail_positions)}')


def part2():
    start_position = (0, 0)
    tail_positions = {start_position}
    knot_positions = [start_position for _ in range(10)]

    with open('dag 9/input.txt') as motions:
        for motion in motions:
            parts = motion.split()
            direction, num_steps = DIRECTIONS[parts[0]], int(parts[1])
            delta_x, delta_y = direction

            for _ in range(num_steps):
                head_x, head_y = knot_positions[0]
                knot_positions[0] = (head_x + delta_x, head_y + delta_y)

                for i in range(1, len(knot_positions)):
                    knot_x, knot_y = knot_positions[i]
                    knot_in_front_x, knot_in_front_y = knot_positions[i-1]
                    delta_knot_x = delta_knot_y = 0

                    if abs(knot_x - knot_in_front_x) == 2 or abs(knot_y - knot_in_front_y) == 2:
                        delta_knot_x = (
                            1 if knot_in_front_x > knot_x else -1 if knot_in_front_x < knot_x else 0)
                        delta_knot_y = (
                            1 if knot_in_front_y > knot_y else -1 if knot_in_front_y < knot_y else 0)

                    knot_positions[i] = (
                        knot_x + delta_knot_x, knot_y + delta_knot_y)

                tail_positions.add(knot_positions[-1])

            # print(f'Head is at ({head_position[0]}, {head_position[1]})')
            # print(f'Tail is at ({tail_position[0]}, {tail_position[1]})')

    print(f'Num positions {len(tail_positions)}')


if __name__ == '__main__':
    # part1()
    part2()
