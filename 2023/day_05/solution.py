import sys
from collections import namedtuple
import math

Mapping = namedtuple('Mapping', ['lower', 'upper', 'offset'])


def get_maps(almanac: list[str]) -> list[list[Mapping]]:
    i = 2
    maps = []
    while i < len(almanac):
        if almanac[i]:
            category_map = []
            j = i+1
            while j < len(almanac) and almanac[j]:
                destination_start, source_start, range = [int(n) for n in almanac[j].split()]
                mapping = Mapping(
                    lower=source_start,
                    upper=source_start+range-1,
                    offset=destination_start-source_start)
                category_map.append(mapping)
                j += 1
            i = j
            maps.append(category_map)
        else:
            i += 1
    return maps


def starts_in_map_range(seed_range, map_range):
    seed_start, _ = seed_range
    map_start, map_end = map_range
    return map_start <= seed_start <= map_end


def ends_in_map_range(seed_range, map_range):
    _, seed_end = seed_range
    map_start, map_end = map_range
    return map_start <= seed_end <= map_end


def is_fully_within_map_range(seed_range, map_range):
    return starts_in_map_range(seed_range, map_range) and ends_in_map_range(seed_range, map_range)


def split_range(seed_range, point, starts):
    seed_start, seed_end = seed_range
    if starts:
        return (seed_start, point), (point+1, seed_end)
    else:
        return (seed_start, point-1), (point, seed_end)


def map_range(seed_range, mapping):
    map_range = mapping.lower, mapping.upper
    numeric_range, is_mapped = seed_range

    if is_mapped:
        return [seed_range]

    if is_fully_within_map_range(numeric_range, map_range):
        mapped_range = numeric_range[0]+mapping.offset, numeric_range[1]+mapping.offset
        return [(mapped_range, True)]
    elif starts_in_map_range(numeric_range, map_range):
        covered, uncovered = split_range(numeric_range, mapping.upper, starts=True)
        mapped_covered = covered[0]+mapping.offset, covered[1]+mapping.offset
        return [(mapped_covered, True), (uncovered, False)]
    elif ends_in_map_range(numeric_range, map_range):
        uncovered, covered = split_range(numeric_range, mapping.lower, starts=False)
        mapped_covered = covered[0]+mapping.offset, covered[1]+mapping.offset
        return [(mapped_covered, True), (uncovered, False)]
    else:
        return [seed_range]


def map_ranges(seed_ranges, mapping):
    mapped_ranges = []
    for seed_range in seed_ranges:
        mapped_ranges += map_range(seed_range, mapping)
    return mapped_ranges


def main():
    filename = sys.argv[1]
    with open(filename) as almanac_file:
        almanac = almanac_file.read().splitlines()

    initial_seed_ranges = [int(s) for s in almanac[0].split(':')[1].split()]
    maps = get_maps(almanac)
    min_location = math.inf

    for i in range(0, len(initial_seed_ranges), 2):
        initial_seed_range = initial_seed_ranges[i], initial_seed_ranges[i]+initial_seed_ranges[i+1]-1
        seed_ranges = [(initial_seed_range, False)]
        for map in maps:
            for mapping in map:
                seed_ranges = map_ranges(seed_ranges, mapping)
            seed_ranges = [(num_range, False) for num_range, _ in seed_ranges]
        min_location_in_batch = min(range_start for (range_start, _), _ in seed_ranges)
        min_location = min(min_location, min_location_in_batch)

    print(min_location)


if __name__ == '__main__':
    mapping = Mapping(50, 60, 100)
    seed_range = ((52, 75), False)
    f = map_range(seed_range, mapping)
    main()
