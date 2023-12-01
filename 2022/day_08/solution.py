from functools import reduce

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def is_visible(i, j, tree_grid):
    height = tree_grid[i][j]
    for direction in DIRECTIONS:
        x, y = j, i
        visible = True
        x_delta, y_delta = direction
        while 0 <= y + y_delta < len(tree_grid) and 0 <= x + x_delta < len(tree_grid[0]):
            y += y_delta
            x += x_delta

            other_height = tree_grid[y][x]
            if other_height >= height:
                visible = False

        if visible:
            return True

    return False


def get_scenic_score(i, j, tree_grid):
    height = tree_grid[i][j]
    viewing_distances = []

    for direction in DIRECTIONS:
        x, y = j, i
        viewing_distance = 0
        x_delta, y_delta = direction

        while 0 <= y + y_delta < len(tree_grid) and 0 <= x + x_delta < len(tree_grid[0]):
            y += y_delta
            x += x_delta
            viewing_distance += 1

            other_height = tree_grid[y][x]
            if other_height >= height:
                break


        viewing_distances.append(viewing_distance)

    return reduce(lambda x, y: x*y, viewing_distances)


def get_num_visible_trees(tree_grid):
    num_visible = 0
    num_rows, num_columns = len(tree_grid), len(tree_grid[0])
    for i in range(num_rows):
        for j in range(num_columns):
            if i == 0 or i == num_rows-1 or j == 0 or j == num_columns-1:
                num_visible += 1
            else:
                num_visible += is_visible(i, j, tree_grid)
    return num_visible


def get_most_scenic(tree_grid):
    num_rows, num_columns = len(tree_grid), len(tree_grid[0])
    max_score = 0
    for i in range(num_rows):
        for j in range(num_columns):
            scenic_score = get_scenic_score(i, j, tree_grid)
            if scenic_score > max_score:
                max_score = scenic_score
    return max_score


def main():
    with open('dag 8/input.txt') as tree_grid_file:
        tree_grid = [[int(height) for height in row]
                     for row in tree_grid_file.read().splitlines()]

    # num_visible = get_num_visible_trees(tree_grid)
    # print(f'num visible {num_visible}')

    most_scenic = get_most_scenic(tree_grid)
    print(f'most scenic {most_scenic}')


if __name__ == '__main__':
    main()
