import sys


class FreeSpaceBlock:
    def __init__(self, position, length):
        self.position = position
        self.length = length
        self.next_free_space_block = None


class FreeSpaceList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, pos, len):
        new_node = FreeSpaceBlock(pos, len)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next_free_space_block = new_node
        self.tail = new_node

    def remove_block(self, block: FreeSpaceBlock):
        if self.head == block:
            self.head = block.next_free_space_block
            return

        curr_block = self.head
        while curr_block.next_free_space_block != block:
            curr_block = curr_block.next_free_space_block
        curr_block.next_free_space_block = block.next_free_space_block


def get_files(disk_map):
    free_space_list = FreeSpaceList()
    file_positions = {}
    file_id = 0
    position = 0
    is_file = True
    initial = {}

    for length in disk_map:
        if is_file:
            file_positions |= {position+i: file_id for i in range(length)}
            initial[file_id] = list(range(position, position+length))
            file_id += 1
        else:
            free_space_list.add(position, length)

        is_file = not is_file
        position += length

    return file_positions, free_space_list, initial


def main():
    filename = sys.argv[1]
    with open(filename) as input_file:
        disk_map = map(int, list(input_file.readline().strip()))

    file_positions, free_space_list, initial = get_files(disk_map)
    file_ids = list(set(file_positions.values()))

    while file_ids:
        file_id = file_ids.pop()
        positions = initial[file_id]

        free_block = free_space_list.head
        while free_block != None:
            if free_block.position < positions[0] and free_block.length >= len(positions):
                for i in range(len(positions)):
                    new_pos = free_block.position + i
                    file_positions[new_pos] = file_id
                    del file_positions[positions[i]]

                if free_block.length == len(positions):
                    free_space_list.remove_block(free_block)
                else:
                    free_block.position += len(positions)
                    free_block.length -= len(positions)
                break

            free_block = free_block.next_free_space_block

    checksum = 0
    for pos, id in file_positions.items():
        checksum += pos * id

    print(checksum)


if __name__ == '__main__':
    main()
