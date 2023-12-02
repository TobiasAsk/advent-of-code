import sys
from collections import defaultdict


def main():
    filename = sys.argv[1]
    replacements = defaultdict(list)

    with open(filename) as molecule_input_file:
        for line in molecule_input_file:
            if len(parts := line.split('=>')) == 2:
                in_molecule, out_molecule = parts
                replacements[in_molecule.strip()].append(out_molecule.strip())
            elif line:
                start_molecule = line

    possible_molecules = set()
    for in_molecule in replacements:
        idx = 0
        while (idx := start_molecule.find(in_molecule, idx)) > -1:
            for repl in replacements[in_molecule]:
                new_mol = start_molecule[:idx] + repl + start_molecule[idx+len(in_molecule):]
                possible_molecules.add(new_mol)
            idx += 1

    print(f'Num distinct molecules is {len(possible_molecules)}')


if __name__ == '__main__':
    main()
