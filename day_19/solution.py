import sys
import re
from functools import cache

BLUEPRINT_REGEX = re.compile(r'(\d+)')


@cache
def get_max_num_geodes(
        costs: tuple[tuple[int]],
        resources: tuple[int],
        robots: tuple[int],
        remaining_minutes: int) -> int:

    if remaining_minutes == 0:
        return resources[3]

    # need something better than a "greedy, always build" strategy since it will just build clay-collecting robots
    build_option = None
    for robot_type, robot_cost in enumerate(costs):
        if all(resources[resource] >= cost
               for resource, cost in enumerate(robot_cost)):

            resources_after_build = tuple(
                resources[r]-robot_cost[r]+robots[r] for r in range(len(resources)))

            robots_after_build = tuple(
                robots[r]+1 if r == robot_type else robots[r] for r in range(len(robots)))

            build_option = resources_after_build, robots_after_build

    resources_no_build = tuple(resources[r]+robots[r]
                               for r in range(len(robots)))

    build_options = [(resources_no_build, robots), build_option] if build_option else [
        (resources_no_build, robots)]

    return max([get_max_num_geodes(
        costs=costs,
        resources=res,
        robots=rob,
        remaining_minutes=remaining_minutes-1) for res, rob in build_options])


def main():
    filename = sys.argv[1]

    with open(filename) as blueprint_file:
        for line in blueprint_file:
            costs = [int(c) for c in BLUEPRINT_REGEX.findall(line)]

            costs = (
                # (ore, clay, obsidian, geode)
                (costs[1], 0, 0, 0),  # ore robot
                (costs[2], 0, 0, 0),  # clay robot
                (costs[3], costs[4], 0, 0),  # obsidian robot
                (costs[5], 0, costs[6], 0)  # geode robot
            )

            starting_resources = (0, 0, 0, 0)  # (ore, clay, obsidian, geode)

            robots = (1, 0, 0, 0)

            max_num_geodes = get_max_num_geodes(
                costs=costs,
                resources=starting_resources,
                robots=robots,
                remaining_minutes=24)

            a = 2


if __name__ == '__main__':
    main()
