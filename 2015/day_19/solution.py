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

        possible_replacements = [r for r in self.get_replacements(molecule)
                                 if len(r) <= len(medicine_molecule)]

        if not possible_replacements:
            return None
        elif medicine_molecule in possible_replacements:
            return 1

        possibilities = [s for new_molecule in possible_replacements if (s := self.get_min_required_steps(
            molecule=new_molecule,
            medicine_molecule=medicine_molecule)) != None]

        return 1 + min(possibilities) if possibilities else None

    def get_replacements(
            self, molecule: str) -> list[tuple[str, int]]:

        new_molecules = []
        worst_molecules = []
        for i in range(len(molecule)):
            for j in range(2):
                if i + j < len(molecule):
                    for repl in self.replacements.get(molecule[i:i+j+1], []):
                        new_molecule = molecule[:i] + repl + molecule[i+j+1:]
                        if molecule[i:i+j+1] in repl:
                            if new_molecule not in worst_molecules:
                                worst_molecules.append(new_molecule)
                        else:
                            if new_molecule not in new_molecules:
                                new_molecules.append(new_molecule)

        return new_molecules + worst_molecules


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
