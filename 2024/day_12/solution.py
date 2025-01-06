import sys

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def get_fence_price(
        region_plot: tuple[int],
        covered_plots: set[tuple[int]],
        garden_plots: list[str]) -> int:

    area = 0
    perimeter = 0
    plot_queue = [region_plot]
    start_x, start_y = region_plot
    plant_type = garden_plots[start_y][start_x]
    height, width = len(garden_plots), len(garden_plots[0])

    while plot_queue:
        plot = plot_queue.pop()
        if plot in covered_plots:
            continue
        covered_plots.add(plot)
        x, y = plot
        area += 1

        for dx, dy in DIRECTIONS:
            new_x, new_y = x+dx, y+dy
            if 0 <= new_x < width and 0 <= new_y < height:
                if garden_plots[new_y][new_x] == plant_type:
                    if (new_x, new_y) not in covered_plots:
                        plot_queue.append((new_x, new_y))
                else:
                    perimeter += 1
            else:
                perimeter += 1

    return area * perimeter


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
                total_price += get_fence_price((x, y), covered_plots, garden_plots)
    print(total_price)


if __name__ == '__main__':
    main()
