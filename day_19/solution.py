import sys
import re
from enum import Enum
from functools import cache

BLUEPRINT_REGEX = re.compile(r'(\d+)')


class Resource(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4


def get_max_num_geodes(
        costs: dict[Resource, dict[Resource, int]],
        resources: dict[Resource, int],
        robots: dict[Resource, int],
        remaining_minutes: int) -> int:

    if remaining_minutes == 0:
        return resources[Resource.GEODE]

    resources_no_build = {r: resources[r]+robots[r] for r in robots}
    
    options = []
    for robot_type, robot_cost in costs.items():
        if all(resources[resource] >= cost
               for resource, cost in robot_cost.items()):

            resources_after_build = {
                r: resources[r]-robot_cost.get(r, 0) for r in resources}

            robots_afer_build = {
                r: robots[r]+1 if r == robot_type else robots[r] for r in robots}

            num_geodes = get_max_num_geodes(
                costs=costs,
                resources=resources_after_build,
                robots=robots_afer_build,
                remaining_minutes=remaining_minutes-1
            )

            options.append(num_geodes)


    no_build_option = get_max_num_geodes(
        costs=costs,
        resources=resources_no_build,
        robots=robots,
        remaining_minutes=remaining_minutes-1)

    return max(options + [no_build_option])


def main():
    filename = sys.argv[1]

    with open(filename) as blueprint_file:
        for line in blueprint_file:
            costs = [int(c) for c in BLUEPRINT_REGEX.findall(line)]

            costs = {
                Resource.ORE: {
                    Resource.ORE: costs[1]
                },
                Resource.CLAY: {
                    Resource.ORE: costs[2]
                },
                Resource.OBSIDIAN: {
                    Resource.ORE: costs[3],
                    Resource.CLAY: costs[4]
                },
                Resource.GEODE: {
                    Resource.ORE: costs[5],
                    Resource.OBSIDIAN: costs[6]
                }
            }

            starting_resources = {
                Resource.ORE: 0,
                Resource.CLAY: 0,
                Resource.OBSIDIAN: 0,
                Resource.GEODE: 0
            }

            robots = {
                Resource.ORE: 1,
                Resource.CLAY: 0,
                Resource.OBSIDIAN: 0,
                Resource.GEODE: 0
            }

            max_num_geodes = get_max_num_geodes(
                costs=costs,
                resources=starting_resources,
                robots=robots,
                remaining_minutes=24)


if __name__ == '__main__':
    main()
