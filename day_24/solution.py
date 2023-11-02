import sys
from collections import namedtuple
from dataclasses import dataclass
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
        blizzards: frozenset[Blizzard],
        valley_map: list[str]) -> frozenset[Blizzard]:

    moved: list[Blizzard] = []
    for blizzard in blizzards:
        new_position = get_new_position(blizzard, valley_map)

        moved.append(Blizzard(
            position=new_position,
            direction=blizzard.direction))

    return frozenset(moved)


def get_new_position(
        blizzard: Blizzard,
        valley_map: list[str]) -> tuple[int]:

    x, y = blizzard.position
    dx, dy = MOVE_DELTAS[blizzard.direction]
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    return ((x+dx, y+dy) if valley_map[y+dy][x+dx] != '#' else
            ((x+2*dx) % valley_width + dx, (y+2*dy) % valley_height + dy))


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

    def __lt__(self, other):
        if self.expected_cost < other.expected_cost:
            return True
        elif self.expected_cost == other.expected_cost:
            return self.estimated_distance_to_goal <= other.estimated_distance_to_goal
        else:
            return False

    def get_successors(self) -> list:
        moves = []
        x, y = self.expedition_position
        moved_blizzards = move_blizzards(self.blizzards, self.valley_map)
        next_blizzard_positions = {b.position for b in moved_blizzards}

        for dx, dy in MOVE_DELTAS:  # move
            new_exp_pos = (x+dx, y+dy)
            # can loop around due to negative indexing but it's fine
            if self.valley_map[y+dy][x+dx] != '#' and new_exp_pos not in next_blizzard_positions:
                moves.append(SearchNode(
                    blizzards=moved_blizzards,
                    expedition_position=new_exp_pos,
                    valley_map=self.valley_map,
                    goal_position=self.goal_position
                ))

        if self.expedition_position not in next_blizzard_positions:  # wait
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
            if (col, row) in blizzard_positions:
                blizzard = next(b for b in blizzards if b.position == (col, row))
                print(DIRECTIONS[blizzard.direction], end='')
            else:
                print('E' if (col, row) == expedition_position else '#' if col in [0, valley_width-1]
                      or row in [0, valley_height-1] else '.', end='')
        print()


def get_blizzards(valley_map) -> frozenset[Blizzard]:
    blizzards = set()
    valley_height, valley_width = len(valley_map), len(valley_map[0])

    for row in range(valley_height):
        for col in range(valley_width):
            char = valley_map[row][col]

            if char in DIRECTIONS:
                blizzards.add(Blizzard(
                    position=(col, row),
                    direction=DIRECTIONS.index(char)))

    return frozenset(blizzards)


def attach_and_eval(C: SearchNode, P: SearchNode, arc_cost):
    C.parent = P
    C.distance_from_root = P.distance_from_root + arc_cost
    C.compute_heuristic()
    C.expected_cost = C.distance_from_root + C.estimated_distance_to_goal


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

    open_nodes: list[SearchNode] = [initial_node]
    while open_nodes:
        current_node = heappop(open_nodes)
        current_node.status = False

        if current_node.expedition_position == current_node.goal_position:
            return current_node

        for successor in current_node.get_successors():
            if successor.status == None:
                attach_and_eval(successor, current_node, arc_cost)
                heappush(open_nodes, successor)
                successor.status = True

            elif current_node.distance_from_root + arc_cost < successor.distance_from_root:
                attach_and_eval(successor, current_node, arc_cost)
                heapify(open_nodes)


def main():
    filename = sys.argv[1]
    with open(filename) as valley_map_file:
        valley_map = valley_map_file.read().splitlines()

    blizzards = get_blizzards(valley_map)
    expedition_position = (1, 0)
    # goal_position = (100, 36)
    goal_position = (6, 5)
    goal_node = search(blizzards, expedition_position, valley_map, goal_position, 1)
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
