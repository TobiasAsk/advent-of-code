import sys


class FreeSpaceBlock:
    def __init__(self, pos):
        self.pos = pos
        self.next_free_space_block = None


class FreeSpaceList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, free_block):
        new_node = FreeSpaceBlock(free_block)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next_free_space_block = new_node
        self.tail = new_node

    def remove_first_node(self):
        if (self.head == None):
            return

        self.head = self.head.next_free_space_block


def get_files(disk_map):
    free_space_list = FreeSpaceList()
    file_positions = {}
    file_id = 0
    position = 0
    is_file = True

    for length in disk_map:
        if is_file:
            file_positions |= {position+i: file_id for i in range(length)}
            file_id += 1
        else:
            for i in range(length):
                free_space_list.add(position+i)

        is_file = not is_file
        position += length

    return file_positions, free_space_list


def main():
    filename = sys.argv[1]
    with open(filename) as input_file:
        disk_map = map(int, list(input_file.readline().strip()))

    file_positions, free_space_list = get_files(disk_map)
    initial_positions = list(file_positions.keys())

    while True:
        end_key = initial_positions.pop()
        end_block = file_positions[end_key]
        new_pos = free_space_list.head.pos
        if new_pos > end_key:
            break
        file_positions[new_pos] = end_block
        free_space_list.remove_first_node()
        del file_positions[end_key]

    checksum = 0
    for pos, id in file_positions.items():
        checksum += pos * id

    print(checksum)


if __name__ == '__main__':
    main()
