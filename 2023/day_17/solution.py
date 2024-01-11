import sys
from dataclasses import dataclass
from heapq import *

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


@dataclass
class LavaCitySearchNode:
    heading: int
    lava_map: list[list[int]]
    crucible_position: tuple[int]
    num_consecutive_straight_moves: int

    distance_from_root: int = 0  # g
    estimated_distance_to_goal: int = 0  # h
    expected_cost: int = 0  # f
    parent: None = None
    status: bool = None

    def __lt__(self, other):
        return self.expected_cost < other.expected_cost

    def compute_heuristic(self) -> None:
        x, y = self.crucible_position
        goal_x, goal_y = len(self.lava_map[0])-1, len(self.lava_map)-1
        self.estimated_distance_to_goal = goal_x - x + goal_y - y

    def __hash__(self) -> int:
        return hash((self.heading, self.num_consecutive_straight_moves) + self.crucible_position)

    def get_successors(self) -> list:
        moves = []
        x, y = self.crucible_position
        height, width = len(self.lava_map), len(self.lava_map[0])

        for i in [-1, 0, 1]:
            next_dir_idx = (self.heading+i) % len(DIRECTIONS)
            next_dir = DIRECTIONS[next_dir_idx]
            dx, dy = next_dir
            if 0 <= x+dx < width and 0 <= y+dy < height:
                if (next_dir_idx != self.heading or
                        (next_dir_idx == self.heading and self.num_consecutive_straight_moves < 3)):

                    next_num_consecutive = (1 if next_dir_idx != self.heading
                                            else self.num_consecutive_straight_moves+1)

                    successor_node = LavaCitySearchNode(
                        heading=next_dir_idx,
                        lava_map=self.lava_map,
                        crucible_position=(x+dx, y+dy),
                        num_consecutive_straight_moves=next_num_consecutive
                    )
                    moves.append(successor_node)

        return moves


def extract_solution(node: LavaCitySearchNode, lava_map):
    least_heat_loss = 0
    n = node
    path = []
    while n.parent != None:
        x, y = n.crucible_position
        least_heat_loss += lava_map[y][x]
        path.append(n.crucible_position)
        n = n.parent
    return least_heat_loss, path


def attach_and_eval(child: LavaCitySearchNode, parent: LavaCitySearchNode, heat_loss):
    child.parent = parent
    child.distance_from_root = parent.distance_from_root + heat_loss
    child.compute_heuristic()
    child.expected_cost = child.distance_from_root + child.estimated_distance_to_goal


def get_initial_node(lava_map):

    initial_node = LavaCitySearchNode(
        heading=0,
        lava_map=lava_map,
        crucible_position=(0, 0),
        num_consecutive_straight_moves=0)

    initial_node.distance_from_root = 0
    initial_node.compute_heuristic()
    initial_node.expected_cost = initial_node.estimated_distance_to_goal

    return initial_node


def search(lava_map: list[list[int]]):
    initial_node = get_initial_node(lava_map)
    open_nodes: list[LavaCitySearchNode] = [initial_node]
    height, width = len(lava_map), len(lava_map[0])
    generated_nodes = {hash(initial_node): initial_node}

    while open_nodes:
        current_node = heappop(open_nodes)
        current_node.status = False

        if current_node.crucible_position == (width-1, height-1):
            return extract_solution(current_node, lava_map)

        for successor in current_node.get_successors():
            node_hash = hash(successor)
            if node_hash in generated_nodes:
                successor = generated_nodes[node_hash]
            else:
                generated_nodes[node_hash] = successor

            successor_x, successor_y = successor.crucible_position
            heat_loss = lava_map[successor_y][successor_x]

            if successor.status == None:
                attach_and_eval(successor, current_node, heat_loss)
                heappush(open_nodes, successor)
                successor.status = True

            elif current_node.distance_from_root + heat_loss < successor.distance_from_root:
                attach_and_eval(successor, current_node, heat_loss)


def print_path(path, lava_map):
    height, width = len(lava_map), len(lava_map[0])
    for y in range(height):
        print(''.join('#' if (x, y) in path else str(lava_map[y][x]) for x in range(width)))
    print()


def main():
    filename = sys.argv[1]
    with open(filename) as map_file:
        lava_map = []
        for line in map_file.read().splitlines():
            lava_map.append([int(d) for d in line])

    heat_loss, path = search(lava_map)
    print(heat_loss)


if __name__ == '__main__':
    main()
