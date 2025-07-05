import sys
from dataclasses import dataclass
import heapq
import math

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


@dataclass
class MemorySpace:
    byte_positions: list[tuple[int]]
    width: int = 71
    height: int = 71
    start_coordinates: tuple[int] = 0, 0
    exit_coordinates: tuple[int] = 70, 70

    def get_next_positions(self, position: tuple[int]) -> list[tuple[int]]:
        positions = []
        x, y = position
        for dx, dy in DIRECTIONS:
            if (0 <= x+dx < self.width and 0 <= y+dy < self.height and
                    (x+dx, y+dy) not in self.byte_positions):
                positions.append((x+dx, y+dy))
        return positions

    def length_of_shortest_path_to_exit(self) -> int:
        start_node = self.start_coordinates
        distance = {start_node: 0}
        frontier = [(0, start_node)]
        expanded = set()

        while frontier:
            dist, pos = heapq.heappop(frontier)

            if pos == self.exit_coordinates:
                return dist

            if pos in expanded:
                continue

            expanded.add(pos)

            for next_pos in self.get_next_positions(pos):
                distance_to_neighbor = distance[pos] + 1
                alternative_dist = distance.get(next_pos, math.inf)

                if distance_to_neighbor < alternative_dist:
                    distance[next_pos] = distance_to_neighbor

                heapq.heappush(frontier, (distance_to_neighbor, next_pos))

        return -1


def main():
    filename = sys.argv[1]
    with open(filename) as byte_position_file:
        byte_positions = [tuple(int(c) for c in line.split(','))
                          for line in byte_position_file]

    for num_bytes in range(2800, len(byte_positions)):
        memory_space = MemorySpace(byte_positions[:num_bytes])
        num_steps = memory_space.length_of_shortest_path_to_exit()
        if num_steps == -1:
            print(byte_positions[num_bytes-1])
            break


if __name__ == '__main__':
    main()
