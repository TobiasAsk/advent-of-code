MOVES = [(0, 1), (-1, 1), (1, 1)]
START_POS = (500, 0)


def get_points(path):
    points = []
    for coord in path.split('->'):
        str_x, str_y = coord.split(',')
        points.append((int(str_x), int(str_y)))
    return points


def get_rock_coordinates(paths):
    coords = set()
    lowest_point_y = 0

    for path in paths:
        for i in range(len(path)-1):
            x_first, y_first = path[i]
            x_last, y_last = path[i+1]

            if y_first > lowest_point_y:
                lowest_point_y = y_first

            delta_x = 1 if x_last > x_first else -1 if x_last < x_first else 0
            delta_y = 1 if y_last > y_first else -1 if y_last < y_first else 0

            rock_x, rock_y = x_first, y_first
            coords.add((rock_x, rock_y))

            while rock_x != x_last or rock_y != y_last:
                rock_x += delta_x
                rock_y += delta_y

                coords.add((rock_x, rock_y))

    return coords, lowest_point_y


def part1():
    paths = []
    with open('dag 14/input.txt') as scan:
        for path in scan:
            points = get_points(path)
            paths.append(points)

    rock_coordinates, lowest_point_y = get_rock_coordinates(paths)
    sand_coordinates = set()

    while True:
        sand_unit_position = START_POS
        at_rest = False

        while not at_rest and sand_unit_position[1] < lowest_point_y:
            unit_x, unit_y = sand_unit_position
            for move in MOVES:
                delta_x, delta_y = move
                candidate_position = (unit_x + delta_x, unit_y + delta_y)
                if not (candidate_position in rock_coordinates or candidate_position in sand_coordinates):
                    sand_unit_position = candidate_position
                    break

            at_rest = (unit_x, unit_y) == sand_unit_position

        if at_rest:
            sand_coordinates.add(sand_unit_position)
        else:
            break
    
    print(f'Num units is {len(sand_coordinates)}')

def part2():
    paths = []
    with open('dag 14/input.txt') as scan:
        for path in scan:
            points = get_points(path)
            paths.append(points)

    rock_coordinates, lowest_point_y = get_rock_coordinates(paths)
    sand_coordinates = set()

    while not START_POS in sand_coordinates:
        sand_unit_position = START_POS
        at_rest = False

        while not at_rest:
            unit_x, unit_y = sand_unit_position
            for move in MOVES:
                delta_x, delta_y = move
                candidate_position = (unit_x + delta_x, unit_y + delta_y)
                if not (candidate_position in rock_coordinates or candidate_position in sand_coordinates
                        or candidate_position[1] > lowest_point_y + 1):
                    sand_unit_position = candidate_position
                    break

            at_rest = (unit_x, unit_y) == sand_unit_position

        sand_coordinates.add(sand_unit_position)
    
    print(f'Num units is {len(sand_coordinates)}')

if __name__ == '__main__':
    # part1()
    part2()