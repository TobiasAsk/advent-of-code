import sys
from collections import namedtuple
from dataclasses import dataclass, field
from heapq import *


Blizzard = namedtuple('blizzard', ['position', 'direction'])
DIRECTIONS = '>v<^'
MOVE_DELTAS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


def move_blizzards(
        blizzards: list[Blizzard],
        valley_map: list[str]) -> list[Blizzard]:

    bounds = len(valley_map), len(valley_map[0])
    return [Blizzard(
        position=get_new_position(b, bounds),
        direction=b.direction)
        for b in blizzards]


def get_new_position(
        blizzard: Blizzard,
        bounds: tuple[int]) -> tuple[int]:

    valley_height, valley_width = bounds
    if blizzard.direction == 0:
        def edge(p): return (p + 1) % valley_width == 0
        return (blizzard.position + 1 if not edge(blizzard.position + 1) else
                blizzard.position - valley_width + 3)

    elif blizzard.direction == 1:
        def edge(p): return p > (valley_height - 1)*valley_width
        return (blizzard.position + valley_width if not edge(blizzard.position + valley_width) else
                blizzard.position % valley_width + valley_width)

    if blizzard.direction == 2:
        def edge(p): return p % valley_width == 0
        return (blizzard.position - 1 if not edge(blizzard.position - 1) else
                blizzard.position + valley_width - 3)

    elif blizzard.direction == 3:
        def edge(p): return p < valley_width
        return (blizzard.position - valley_width if not edge(blizzard.position - valley_width) else
                blizzard.position % valley_width + (valley_height-2)*valley_width)


@dataclass
class SearchNode:
    blizzards: list[Blizzard]
    expedition_position: tuple[int]
    valley_map: list[str]
    goal_position: tuple[int]

    distance_from_root: int = 0  # g
    estimated_distance_to_goal: int = 0  # h
    expected_cost: int = 0  # f
    parent: None = None
    status: bool = None
    kids: list = field(default_factory=list)

    def __lt__(self, other):
        return self.expected_cost < other.expected_cost

    def __hash__(self) -> int:
        return hash(self.expedition_position) + sum(hash(b.position) for b in self.blizzards)

    def get_successors(self) -> list:
        moves = []
        x, y = self.expedition_position
        moved_blizzards = move_blizzards(self.blizzards, self.valley_map)
        next_blizzard_positions = {b.position for b in moved_blizzards}
        valley_width = len(self.valley_map[0])

        for dx, dy in MOVE_DELTAS:  # move
            new_exp_pos = (x+dx, y+dy)

            flat_pos = (y+dy) * valley_width + x+dx
            # can loop around due to negative indexing but it's fine
            if self.valley_map[y+dy][x+dx] != '#' and flat_pos not in next_blizzard_positions:
                moves.append(SearchNode(
                    blizzards=moved_blizzards,
                    expedition_position=new_exp_pos,
                    valley_map=self.valley_map,
                    goal_position=self.goal_position
                ))

        flat_current_pos = y*valley_width + x

        if flat_current_pos not in next_blizzard_positions:  # wait
            moves.append(SearchNode(
                blizzards=moved_blizzards,
                expedition_position=self.expedition_position,
                valley_map=self.valley_map,
                goal_position=self.goal_position
            ))

        return moves

    def compute_heuristic(self) -> None:
        x, y = self.expedition_position
        goal_x, goal_y = self.goal_position
        self.estimated_distance_to_goal = goal_x - x + goal_y - y


def print_map(
        blizzards: list[Blizzard],
        valley_map,
        expedition_position):

    valley_height, valley_width = len(valley_map), len(valley_map[0])
    blizzard_positions = [b.position for b in blizzards]

    for row in range(valley_height):
        for col in range(valley_width):
            pos = row*valley_width + col

            if pos in blizzard_positions:
                blizzard = next(b for b in blizzards if b.position == pos)
                print(DIRECTIONS[blizzard.direction], end='')
            else:
                print('E' if (col, row) == expedition_position else '#' if col in [0, valley_width-1]
                      or row in [0, valley_height-1] else '.', end='')
        print()


def get_blizzards(valley_map) -> list[Blizzard]:
    blizzards = []
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    for row in range(valley_height):
        for col in range(valley_width):
            char = valley_map[row][col]

            if char in DIRECTIONS:
                blizzards.append(Blizzard(
                    position=row*valley_width+col,
                    direction=DIRECTIONS.index(char)))

    return blizzards


def attach_and_eval(C: SearchNode, P: SearchNode, arc_cost):
    C.parent = P
    C.distance_from_root = P.distance_from_root + arc_cost
    C.compute_heuristic()
    C.expected_cost = C.distance_from_root + C.estimated_distance_to_goal


def propagate_path_improvements(node: SearchNode, arc_cost):
    for child in node.kids:
        if node.distance_from_root + arc_cost < child.distance_from_root:
            child.parent = node
            child.distance_from_root = node.distance_from_root + arc_cost
            child.expected_cost = child.distance_from_root + child.estimated_distance_to_goal
            propagate_path_improvements(child, arc_cost)


def search(blizzards: list[Blizzard],
           expedition_position: tuple[int],
           valley_map: list[str],
           goal_position: tuple[int],
           arc_cost=0.2):

    initial_node = SearchNode(
        blizzards=blizzards,
        expedition_position=expedition_position,
        valley_map=valley_map,
        goal_position=goal_position
    )

    initial_node.distance_from_root = 0
    initial_node.compute_heuristic()
    initial_node.expected_cost = initial_node.estimated_distance_to_goal

    generated_nodes = {
        hash(initial_node): initial_node
    }

    open_nodes: list[SearchNode] = [initial_node]
    while open_nodes:
        current_node = heappop(open_nodes)
        current_node.status = False

        if current_node.expedition_position == current_node.goal_position:
            return current_node

        for successor in current_node.get_successors():
            state_hash = hash(successor)
            if state_hash in generated_nodes:
                successor = generated_nodes[state_hash]
            else:
                generated_nodes[state_hash] = successor

            current_node.kids.append(successor)

            if successor.status == None:
                attach_and_eval(successor, current_node, arc_cost)
                heappush(open_nodes, successor)
                successor.status = True

            elif current_node.distance_from_root + arc_cost < successor.distance_from_root:
                attach_and_eval(successor, current_node, arc_cost)
                if successor.status == False:
                    propagate_path_improvements(successor, arc_cost)
                open_nodes.sort()


def get_goal_position(valley_map):
    x = valley_map[-1].index('.')
    return x, len(valley_map)-1


def main():
    filename = sys.argv[1]
    with open(filename) as valley_map_file:
        valley_map = valley_map_file.read().splitlines()

    blizzards = get_blizzards(valley_map)
    expedition_position = (1, 0)

    goal_position = get_goal_position(valley_map)
    goal_node = search(blizzards, expedition_position, valley_map, goal_position, 0.6)
    solution = build_solution(goal_node)
    print(len(solution)-1)


def build_solution(node):
    solution = []
    solution.append(node)
    n = node

    while n.parent != None:
        n = n.parent
        solution.append(n)
    return solution


if __name__ == '__main__':
    main()
