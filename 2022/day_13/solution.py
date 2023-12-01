import functools


def parse_packet(packet_string: str):
    packet = []
    i = 0

    while i < len(packet_string):
        char = packet_string[i]
        if char == '[':
            sub_list, distance = parse_packet(packet_string[i+1:])
            packet.append(sub_list)
            i += distance

        elif char.isdigit():
            integer_start = i
            while i + 1 < len(packet_string) and packet_string[i+1].isdigit():
                i += 1
            packet.append(int(packet_string[integer_start:i+1]))

        elif char == ']':
            i += 1
            break

        i += 1

    return packet, i


def compare(packet, other_packet):
    length = min(len(packet), len(other_packet))
    for i in range(length):
        left, right = packet[i], other_packet[i]
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                continue
            return 1 if left > right else -1
        elif isinstance(left, list) and isinstance(right, int):
            res = compare(left, [right])
            if res != 0:
                return res
        elif isinstance(left, int) and isinstance(right, list):
            res = compare([left], right)
            if res != 0:
                return res
        else:
            res = compare(left, right)
            if res != 0:
                return res

    if len(packet) == len(other_packet):
        return 0

    return 1 if len(packet) > len(other_packet) else -1


def get_pairs(packet_input: list[str]):
    pairs = []
    for i in range(0, len(packet_input), 2):
        packet, other_packet = parse_packet(
            packet_input[i][1:-1])[0], parse_packet(packet_input[i+1][1:-1])[0]
        pairs.append((packet, other_packet))
    return pairs


def part1():
    with open('dag 13/example_input.txt') as packets_file:
        packet_input = [l for l in packets_file.read().splitlines() if l]

    indices_sum = 0
    pairs = get_pairs(packet_input)

    for pair_num, pair in enumerate(pairs):
        packet, other_packet = pair
        if compare(packet, other_packet):
            indices_sum += (pair_num + 1)

    print(f'Sum is {indices_sum}')


def get_all_packets(packet_input):
    packets = []
    for line in packet_input:
        packets.append(parse_packet(line[1:-1])[0])
    return packets


def part2():
    with open('dag 13/input.txt') as packets_file:
        packet_input = [l for l in packets_file.read().splitlines() if l]

    all_packets = get_all_packets(packet_input)
    divider_packets = [[[2]], [[6]]]
    all_packets.extend(divider_packets)
    sorted_packets = sorted(all_packets, key=functools.cmp_to_key(compare))
    index_first, index_second = sorted_packets.index(
        divider_packets[0]), sorted_packets.index(divider_packets[1])
    print(f'Decoder key is {(index_first+1)*(index_second+1)}')


if __name__ == '__main__':
    # part1()
    part2()
