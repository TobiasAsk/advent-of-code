import sys


def main():
    filename = sys.argv[1]
    with open(filename) as id_ranges_file:
        id_ranges_raw = id_ranges_file.readline().split(',')

    id_ranges = [tuple(int(x) for x in r.split('-')) for r in id_ranges_raw]
    invalid_ids = set()
    for start, stop in id_ranges:
        for num in range(start, stop+1):
            str_num = str(num)
            mid = len(str_num) // 2
            for chunk_size in range(1, mid+1):
                chunks = [str_num[i:i+chunk_size] for i in range(0, len(str_num), chunk_size)]
                if all(chunks[i] == chunks[i+1] for i in range(len(chunks)-1)):
                    invalid_ids.add(num)
    print(sum(invalid_ids))


if __name__ == '__main__':
    main()
