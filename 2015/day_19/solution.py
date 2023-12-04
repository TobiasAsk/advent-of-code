import sys
from collections import defaultdict
from functools import cache


class Machine:

    def __init__(self, replacements: dict):
        self.replacements = replacements

    @cache
    def get_min_required_steps(
            self, molecule: str,
            medicine_molecule: str):

        possible_replacements = self.get_possible_replacements(molecule, medicine_molecule)
        if not possible_replacements:
            return None
        elif medicine_molecule in possible_replacements:
            return 1

        possibilities = [s for replacement in possible_replacements if (s := self.get_min_required_steps(
            molecule=replacement,
            medicine_molecule=medicine_molecule)) != None]

        return 1 + min(possibilities) if possibilities else None

    def get_possible_replacements(
            self, molecule, medicine_molecule):

        possible_replacements = []
        for in_molecule in self.replacements:
            idx = 0
            while (idx := molecule.find(in_molecule, idx)) > -1:
                for repl in self.replacements[in_molecule]:
                    new_mol = molecule[:idx] + repl + molecule[idx+len(in_molecule):]
                    if len(new_mol) <= len(medicine_molecule):
                        possible_replacements.append(new_mol)

                idx += 1

        return possible_replacements


def parse_input(input_lines):
    replacements = defaultdict(list)

    for line in input_lines:
        if len(parts := line.split('=>')) == 2:
            in_molecule, out_molecule = parts
            replacements[in_molecule.strip()].append(out_molecule.strip())

        elif line:
            medicine_molecule = line

    return replacements, medicine_molecule


def main():
    filename = sys.argv[1]

    with open(filename) as molecule_input_file:
        replacements, medicine_molecule = parse_input(molecule_input_file.read().splitlines())

    machine = Machine(replacements)
    min_steps = machine.get_min_required_steps(
        molecule='e',
        medicine_molecule=medicine_molecule
    )
    print(min_steps)


if __name__ == '__main__':
    main()
