import sys
from collections import namedtuple

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


def main():
    filename = sys.argv[1]
    with open(filename) as almanac_file:
        almanac = almanac_file.read().splitlines()

    seeds = [int(s) for s in almanac[0].split(':')[1].split()]
    maps = get_maps(almanac)
    lowest_location = 1000000000000
    i = 0
    while i < len(seeds):
        resource_id = seeds[i]
        for map in maps:
            for mapping in map:
                if mapping.lower <= resource_id <= mapping.upper:
                    resource_id += mapping.offset
                    break

        location = resource_id
        if location < lowest_location:
            lowest_location = location
        i += 1

    print(lowest_location)


if __name__ == '__main__':
    main()
