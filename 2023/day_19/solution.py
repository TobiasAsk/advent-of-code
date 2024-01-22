import sys
from dataclasses import dataclass, field
import re

RULE_PATTERN = re.compile(r'([xmas])([<>])(\d+):(\w+)')
WORKFLOW_PATTERN = re.compile(r'(\w+)\{([\w\W]+)\}')
RATING_PATTERN = re.compile(r'\w=\d+')


@dataclass
class Workflow:
    name: str
    rules: list = field(default_factory=list)

    def get_next_workflow(self, part: dict):
        for rule in self.rules:
            if (next_workflow := rule(part)):
                return next_workflow


def parse_rule(rule: str):
    if (pattern_match := RULE_PATTERN.search(rule)):
        category, operator, limit, next_workflow = pattern_match.groups()
        if operator == '>':
            return lambda part: next_workflow if part[category] > int(limit) else None
        else:
            return lambda part: next_workflow if part[category] < int(limit) else None
    else:
        return lambda _: rule


def parse_workflow(raw_workflow) -> Workflow:
    name, raw_rules = WORKFLOW_PATTERN.search(raw_workflow).groups()
    parsed_rules = [parse_rule(r) for r in raw_rules.split(',')]
    return Workflow(name, parsed_rules)


def parse_part(raw_part: str) -> dict:
    ratings = RATING_PATTERN.findall(raw_part)
    pairs = [r.split('=') for r in ratings]
    return {c: int(r) for c, r in pairs}


def main():
    filename = sys.argv[1]
    with open(filename) as workflows_and_parts_file:
        raw_workflows, raw_parts = tuple(p.splitlines() for p in workflows_and_parts_file.read().split('\n\n'))

    workflows: dict[str, Workflow] = {}
    for raw_workflow in raw_workflows:
        workflow = parse_workflow(raw_workflow)
        workflows[workflow.name] = workflow

    parts = [parse_part(p) for p in raw_parts]
    rating_sum = 0

    for part in parts:
        current_workflow = workflows['in']
        while current_workflow:
            next_name = current_workflow.get_next_workflow(part)
            current_workflow = workflows.get(next_name)

        if next_name == 'A':
            rating_sum += sum(r for r in part.values())

    print(rating_sum)


if __name__ == '__main__':
    main()
