import sys
from collections import defaultdict


def parse_input(input_lines):
    replacements = defaultdict(list)

    for line in input_lines:
        if len(parts := line.split('=>')) == 2:
            in_molecule, out_molecule = parts
            replacements[in_molecule.strip()].append(out_molecule.strip())

        elif line:
            medicine_molecule = line

    return replacements, medicine_molecule


def get_min_required_steps(molecule, medicine_molecule, replacements):
    possible_replacements = []
    for in_molecule in replacements:
        idx = 0
        while (idx := molecule.find(in_molecule, idx)) > -1:
            for repl in replacements[in_molecule]:
                new_mol = molecule[:idx] + repl + molecule[idx+len(in_molecule):]

                if new_mol == medicine_molecule:
                    return 1

                elif len(new_mol) <= len(medicine_molecule):
                    possible_replacements.append(new_mol)
            idx += 1

    if not possible_replacements:
        return None

    possibilities = [get_min_required_steps(
        molecule=replacement,
        medicine_molecule=medicine_molecule,
        replacements=replacements) for replacement in possible_replacements]

    return 1 + min(possibilities)


def main():
    filename = sys.argv[1]

    with open(filename) as molecule_input_file:
        replacements, medicine_molecule = parse_input(molecule_input_file.read().splitlines())

    min_steps = get_min_required_steps(
        molecule='e',
        medicine_molecule='HOH',
        replacements=replacements
    )
    print(min_steps)


if __name__ == '__main__':
    main()
