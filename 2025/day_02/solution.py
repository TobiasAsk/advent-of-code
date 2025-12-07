import sys


def main():
    filename = sys.argv[1]
    with open(filename) as id_ranges_file:
        id_ranges_raw = id_ranges_file.readline().split(',')

    id_ranges = [tuple(int(x) for x in r.split('-')) for r in id_ranges_raw]
    invalid_id_sum = 0
    for start, stop in id_ranges:
        for num in range(start, stop+1):
            str_num = str(num)
            mid = len(str_num) // 2
            if str_num[:mid] == str_num[mid:]:
                invalid_id_sum += num
    print(invalid_id_sum)


if __name__ == '__main__':
    main()
