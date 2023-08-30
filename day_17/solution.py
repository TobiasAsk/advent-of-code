import sys

'''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''


ROCKS = [  # X, Y positions relative to bottom left corner. X is from left to right, Y from bottom to top
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
]

CHAMBER_WIDTH = 7
TARGET_NUM_ROCKS = 2022
ROCK_SPAWN_DELTA_X = 2
ROCK_SPAWN_DELTA_Y = 4


def simulate(jet_pattern):
    jet_idx, num_rocks_at_rest, tower_height = 0, 0, 0
    rock_tower = set()

    while num_rocks_at_rest < TARGET_NUM_ROCKS:
        rock_coordinates = [(x+ROCK_SPAWN_DELTA_X, y+ROCK_SPAWN_DELTA_Y+tower_height)
                            for (x, y) in ROCKS[num_rocks_at_rest % 5]]
        falling = False

        while True:
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

            if lowest_rock_point <= tower_height:
                tower_points = set(
                    p for p in rock_tower if p[1] >= lowest_rock_point)
                collision_with_tower = any(
                    point in tower_points for point in next_rock_coordinates)
            else:
                collision_with_tower = False

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
