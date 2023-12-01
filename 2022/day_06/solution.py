def main():
    with open('dag 6/input.txt') as datastream_file:
        datastream = datastream_file.read()

    sequence = ''
    start_of_packet_idx = 0
    for idx, char in enumerate(datastream):
        if len(sequence) < 14:
            sequence += char
        else:
            if len(set(sequence)) == 14:
                start_of_packet_idx = idx
                break
            else:
                sequence = sequence[1:] + char

    print(f'first marker after {start_of_packet_idx}')


if __name__ == '__main__':
    main()
