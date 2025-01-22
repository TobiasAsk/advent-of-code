'''This had me scratching my head for a while. Tried edge walking which nearly worked,
but it struggled with containment cases. Then I gave in and read a bit on reddit, where I found the
brilliantly simple insight that the number of sides is equal to the number of corners. Counting corners
is trivial: just inspect the eight neighbor cells, rotating around with an L. Can have two cases, inner
or outer, depending on the content of the L.

I do flood fill first, then traversal, but it should be possible and more efficient to do both in
one go.'''

import sys

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_num_sides(region: set[tuple[int]]) -> int:
    '''The number of corners equals the number of sides!
    Start anywhere, move through each plot and count the number of corners'''

    num_sides = 0
    for x, y in region:
        for rotation in range(4):
            dx, dy = DIRECTIONS[rotation]
            ccw_dx, ccw_dy = DIRECTIONS[(rotation-1) % 4]
            is_inner_corner = ((x+dx, y+dy) in region and
                               (x+ccw_dx, y+ccw_dy) in region and
                               (x+dx+ccw_dx, y+dy+ccw_dy) not in region)

            is_outer_corner = ((x+dx, y+dy) not in region and
                               (x+ccw_dx, y+ccw_dy) not in region)

            num_sides += is_outer_corner or is_inner_corner

    return num_sides


def get_region(
        region_plot: tuple[int],
        covered_plots: set[tuple[int]],
        garden_plots: list[str]) -> set[tuple[int]]:

    region = set()
    plot_queue = [region_plot]
    height, width = len(garden_plots), len(garden_plots[0])
    x, y = region_plot
    plant_type = garden_plots[y][x]

    while plot_queue:
        plot = plot_queue.pop()
        if plot in covered_plots | region:
            continue
        region.add(plot)
        x, y = plot

        for dx, dy in DIRECTIONS:
            new_x, new_y = x+dx, y+dy
            if (0 <= new_x < width and 0 <= new_y < height and
                garden_plots[new_y][new_x] == plant_type and
                    (new_x, new_y) not in covered_plots | region):
                plot_queue.append((new_x, new_y))

    return frozenset(region)


def main():
    filename = sys.argv[1]
    with open(filename) as garden_plot_map_file:
        garden_plots = garden_plot_map_file.read().splitlines()

    height, width = len(garden_plots), len(garden_plots[0])
    covered_plots = set()

    total_price = 0
    for y in range(height):
        for x in range(width):
            if (x, y) not in covered_plots:
                region = get_region((x, y), covered_plots, garden_plots)
                covered_plots |= region
                num_sides = get_num_sides(region)
                total_price += len(region) * num_sides

    print(total_price)


if __name__ == '__main__':
    main()
