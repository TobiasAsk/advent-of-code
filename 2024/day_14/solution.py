import sys
import re
from dataclasses import dataclass
from functools import reduce
from operator import mul
import math

ROBOT_PATTERN = re.compile(r'p=(\d+),(\d+) v=(\-?\d+),(\-?\d+)')
WIDTH, HEIGHT = 101, 103


@dataclass
class Robot:
    position: tuple[int]
    velocity: tuple[int]


def print_robots(robots: list[Robot]):
    positions = [r.position for r in robots]
    for y in range(HEIGHT):
        print(''.join('1' if (x, y) in positions else '.' for x in range(WIDTH)))


def get_safety_score(quad_counts: list[int]) -> int:
    return reduce(mul, quad_counts)


def get_quadrant_num(pos) -> int:
    mid_height, mid_width = HEIGHT // 2, WIDTH // 2
    x, y = pos
    if x < mid_width:
        return 0 if y < mid_height else 3 if y > mid_height else -1
    elif x > mid_width:
        return 1 if y < mid_height else 2 if y > mid_height else -1
    else:
        return -1


def main():
    filename = sys.argv[1]
    robots: list[Robot] = []
    with open(filename) as robot_data_file:
        for robot_config in robot_data_file:
            values = ROBOT_PATTERN.search(robot_config).groups()
            pos_x, pos_y, v_x, v_y = list(map(int, values))
            robot = Robot(position=(pos_x, pos_y), velocity=(v_x, v_y))
            robots.append(robot)

    min_score = math.inf
    tree_time = None

    for i in range(WIDTH*HEIGHT):
        quadrant_counts = [0]*4
        for robot in robots:
            pos_x, pos_y = robot.position
            v_x, v_y = robot.velocity
            new_x = (pos_x+v_x) % WIDTH
            new_y = (pos_y+v_y) % HEIGHT
            robot.position = (new_x, new_y)
            quadrant_num = get_quadrant_num((new_x, new_y))
            if quadrant_num > -1:
                quadrant_counts[quadrant_num] += 1

        safety_score = get_safety_score(quadrant_counts)
        if safety_score < min_score:
            min_score = safety_score
            tree_time = i

    print(tree_time+1)


if __name__ == '__main__':
    main()
