import math

# directions in (delta_x, delta_y) format with inverted Y-axis
DIRECTIONS = [
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0),  # left
    (0, -1)  # up
]


def get_elevation(grid_cell):
    if grid_cell == 'S':
        return 0
    elif grid_cell == 'E':
        return 25
    else:
        return ord(grid_cell) - 97


def get_adjacency_matrix(heightmap, reverse=False):
    width, height = len(heightmap[0]), len(heightmap)
    num_nodes = width * height
    adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for row in range(height):
        for column in range(width):
            node_num = row * width + column
            elevation = get_elevation(heightmap[row][column])

            if heightmap[row][column] == 'E':
                target_location = node_num
            elif heightmap[row][column] == 'S':
                start_location = node_num

            for direction in DIRECTIONS:
                delta_x, delta_y = direction
                if 0 <= row + delta_y < height and 0 <= column + delta_x < width:
                    other_elevation = get_elevation(heightmap[row+delta_y][column+delta_x])
                    other_node_num = (row + delta_y) * width + column + delta_x

                    is_neighbor = (elevation - other_elevation <= 1 if reverse else other_elevation - elevation <= 1)
                    adjacency_matrix[node_num][other_node_num] = int(is_neighbor)

    return adjacency_matrix, start_location, target_location


def get_min(queue, distances):
    min_node = queue[0]
    minimum = distances[min_node]
    for node in queue:
        if distances[node] < minimum:
            min_node = node
            minimum = distances[node]
    return min_node


def part1():
    with open('dag 12/input.txt') as heightmap_file:
        heightmap = heightmap_file.read().splitlines()

    adjacency_matrix, start_location, target_location = get_adjacency_matrix(heightmap)

    dist = [math.inf] * len(adjacency_matrix)
    prev = [None] * len(adjacency_matrix)
    dist[start_location] = 0
    queue = list(range(len(adjacency_matrix)))

    while queue:
        node = get_min(queue, dist)
        if node == target_location:
            path = []
            while node != None:
                path.append(node)
                node = prev[node]
            print(len(path)-1)
            break

        queue.remove(node)
        for other_node in queue:
            if adjacency_matrix[node][other_node]:
                alt = dist[node] + 1
                if alt < dist[other_node]:
                    dist[other_node] = alt
                    prev[other_node] = node


def get_candidates(heightmap):
    width, height = len(heightmap[0]), len(heightmap)
    candidates = []

    for row in range(height):
        for column in range(width):
            if heightmap[row][column] == 'a':
                node_num = row * width + column
                candidates.append(node_num)

    return candidates


def part2():
    # do reverse path search from E to all other squares with inverted neighbor condition (edge u->v if elevation(u) - elevation(v) <= 1)
    # then check all 'a' squares
    # inefficient? shh
    with open('dag 12/input.txt') as heightmap_file:
        heightmap = heightmap_file.read().splitlines()

    adjacency_matrix, _, target_location = get_adjacency_matrix(heightmap, reverse=True)

    dist = [math.inf] * len(adjacency_matrix)
    prev = [None] * len(adjacency_matrix)
    dist[target_location] = 0
    queue = list(range(len(adjacency_matrix)))

    while queue:
        node = get_min(queue, dist)
        queue.remove(node)
        for other_node in queue:
            if adjacency_matrix[node][other_node]:
                alt = dist[node] + 1
                if alt < dist[other_node]:
                    dist[other_node] = alt
                    prev[other_node] = node

    candidate_starting_positions = get_candidates(heightmap)
    distances = [dist[c] for c in candidate_starting_positions]
    print(min(distances))

if __name__ == '__main__':
    # part1()
    part2()
