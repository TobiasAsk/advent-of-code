import sys


ROCKS = [  # X, Y positions relative to bottom left corner. X is from left to right, Y from bottom to top
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
]

CHAMBER_WIDTH = 7
TARGET_NUM_ROCKS = 1000000000000
ROCK_SPAWN_DELTA_X = 2
ROCK_SPAWN_DELTA_Y = 4


def print_chamber(tower_height, tower):
    for row in range(tower_height, max(tower_height-20, 0), -1):
        row_visual = ('|' + ''.join('#' if (x, row)
                      in tower else '.' for x in range(CHAMBER_WIDTH)) + '|')
        print(row_visual)
    print()


def simulate(jet_pattern):
    jet_idx, num_rocks_at_rest, tower_height = 0, 0, 0
    cyclic_count, prev_height, prev_num_rocks = 0, 0, 0
    prev_rock_diff = 0
    rock_tower = set()

    while num_rocks_at_rest < TARGET_NUM_ROCKS:
        rock_coordinates = [(x+ROCK_SPAWN_DELTA_X, y+ROCK_SPAWN_DELTA_Y+tower_height)
                            for (x, y) in ROCKS[num_rocks_at_rest % 5]]
        falling = False

        while True:
            # don't fully understand why this is the cycle indicator, but it works
            if jet_idx == (num_rocks_at_rest % 5) and falling:
                cyclic_count += 1
                if cyclic_count % 4 == 0:  # from manual inspection
                    height_diff = tower_height - prev_height
                    prev_height = tower_height

                    rock_diff = num_rocks_at_rest - prev_num_rocks
                    prev_num_rocks = num_rocks_at_rest

                    if prev_rock_diff == rock_diff:
                        print('Rock pattern is stable, jumping ahead')
                        num_required_cycles = (
                            TARGET_NUM_ROCKS - num_rocks_at_rest) // rock_diff
                        added_height = num_required_cycles * height_diff
                        num_rocks_at_rest += num_required_cycles * rock_diff
                        tower_height += added_height

                        rock_coordinates = [(x, y+added_height)
                                            for (x, y) in rock_coordinates]

                        rock_tower = {(x, y+added_height)
                                      for (x, y) in rock_tower}

                    prev_rock_diff = rock_diff

            if falling:
                next_rock_coordinates = [(x, y-1)
                                         for (x, y) in rock_coordinates]
            else:
                jet_push = jet_pattern[jet_idx]
                delta_x = 1 if jet_push == '>' else -1
                next_rock_coordinates = [(x+delta_x, y)
                                         for (x, y) in rock_coordinates]
                jet_idx = (jet_idx + 1) % len(jet_pattern)

            lowest_rock_point = min(p[1] for p in next_rock_coordinates)

            collision_with_tower = (any(
                point in rock_tower for point in next_rock_coordinates)
                if lowest_rock_point <= tower_height else False)

            chamber_collision = any(
                x < 0 or x >= CHAMBER_WIDTH for (x, _) in next_rock_coordinates)

            collision_with_ground = lowest_rock_point == 0

            if not (collision_with_tower or chamber_collision or collision_with_ground):
                rock_coordinates = next_rock_coordinates
            else:
                if falling:
                    break

            falling = not falling

        rock_tower = rock_tower | {(x, y) for (x, y) in rock_coordinates}
        highest_rock_point = max(y for (_, y) in rock_coordinates)
        tower_height = max(tower_height, highest_rock_point)
        num_rocks_at_rest += 1

    return tower_height


def main():
    input_file = sys.argv[1]
    with open(input_file) as input:
        jet_pattern = input.readline()
        tower_height = simulate(jet_pattern)
        print(f'Tower height is {tower_height}')


if __name__ == '__main__':
    main()
