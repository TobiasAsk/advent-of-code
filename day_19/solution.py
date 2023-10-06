import sys
import re
import math
from functools import cache

BLUEPRINT_REGEX = re.compile(r'(\d+)')


class Blueprint:
    def __init__(self, costs):
        self.costs = costs
        self.best = {}

    @cache
    def get_max_num_geodes(
            self, resources: tuple[int],
            robots: tuple[int],
            remaining_minutes: int) -> int:

        if remaining_minutes == 0:
            return resources[3]

        current = resources[3] + (robots[3]*remaining_minutes)
        if remaining_minutes == 1:
            return current

        if current < self.best.get(remaining_minutes, 0):
            return 0
        
        self.best[remaining_minutes] = current

        options = []
        for robot_type, robot_cost in enumerate(self.costs):
            # can we build this robot right now?
            if all(resources[r] >= robot_cost[r] for r in range(len(resources))):
                resources_after_build = tuple(
                    resources[r]-robot_cost[r]+robots[r] for r in range(len(resources)))

                robots_after_build = tuple(
                    robots[r]+1 if r == robot_type else robots[r] for r in range(len(robots)))

                options.append((resources_after_build, robots_after_build, 1))

            # can we save up for it?
            elif all(robots[r] > 0 for r in range(len(resources)) if robot_cost[r] > 0):
                required_wait_time = 0

                for r in range(len(resources)):
                    wait_time = math.ceil(
                        (robot_cost[r] - resources[r]) / robots[r]) + 1 if robots[r] > 0 else 0
                    required_wait_time = max(required_wait_time, wait_time)

                if remaining_minutes - required_wait_time > 0:
                    resources_after_build = tuple(
                        resources[r]-robot_cost[r]+robots[r]*required_wait_time for r in range(len(resources)))

                    robots_after_build = tuple(
                        robots[r]+1 if r == robot_type else robots[r] for r in range(len(robots)))

                    options.append(
                        (resources_after_build, robots_after_build, required_wait_time))

        return max([self.get_max_num_geodes(
            resources=res,
            robots=rob,
            remaining_minutes=remaining_minutes-wait) for res, rob, wait in options]) if options else current


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

            blueprint = Blueprint(costs)

            starting_resources = (0, 0, 0, 0)  # (ore, clay, obsidian, geode)

            robots = (1, 0, 0, 0)

            max_num_geodes = blueprint.get_max_num_geodes(
                resources=starting_resources,
                robots=robots,
                remaining_minutes=24)

            a = 2


if __name__ == '__main__':
    main()
