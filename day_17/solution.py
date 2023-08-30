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
ROCK_SPAWN_DELTA = (2, 4)


def simulate(jet_pattern):
    rock_idx, jet_idx, num_rocks_at_rest, tower_height = 0, 0, 0, 0
    ground = []
    
    while num_rocks_at_rest < TARGET_NUM_ROCKS:
        spawn_delta_x, spawn_delta_y = ROCK_SPAWN_DELTA
        rock_coordinates = [(x+spawn_delta_x, y+spawn_delta_y+tower_height)
                            for (x, y) in ROCKS[rock_idx]]
        rock_at_rest = False
        while not rock_at_rest:
            # simulate one timestep of rock movement
            if falling:
                rock_coordinates = [(x, y-1)
                                    for (x, y) in rock_coordinates]
            else:
                jet_push = jet_pattern[jet_idx]
                delta_x = (1 if jet_push == '>' and all(
                    x+1 < CHAMBER_WIDTH for (x, _) in rock_coordinates) else -1 if jet_push == '<' and all(
                    x-1 >= 0 for (x, _) in rock_coordinates) else 0)

                if delta_x != 0:
                    rock_coordinates = [(x+delta_x, y)
                                        for (x, y) in rock_coordinates]

                jet_idx = (jet_idx + 1) % len(jet_pattern)

            rock_at_rest = (any(y == 0 for (_, y) in rock_coordinates) or any(y == ground_y for (
                _, y) in rock_coordinates for (_, ground_y) in ground))
            falling = not falling

        # place rock at ground
        ground.extend((x, y+1)
                      for (x, y) in rock_coordinates)
        tower_height = max(y for (_, y) in ground)

        num_rocks_at_rest += 1
        rock_idx = (rock_idx + 1) % len(ROCKS)
    return tower_height


def main():
    input_file = sys.argv[1]
    with open(input_file) as input:
        jet_pattern = input.readline()
        tower_height = simulate(jet_pattern)
        print(f'Tower height is {tower_height}')

if __name__ == '__main__':
    main()
