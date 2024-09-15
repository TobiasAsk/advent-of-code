"""
Represented as a multigraph of workflows with the rules as the edges between them.
I struggled with:
 - wrapping my head around the multiple edges part (hence multigraph). Easy to code (double loop) but hard to realize!
 - handling multiple rules on the same variable ("rating")
 - handling irrelevant rules with looser restrictions than existing bounds
"""

import sys
import re
from collections import namedtuple, defaultdict
from functools import reduce
from operator import mul
import pygraphviz as pgv

RULE_PATTERN = re.compile(r'([xmas])([<>])(\d+):(\w+)')
WORKFLOW_PATTERN = re.compile(r'(\w+)\{([\w\W]+)\}')

Rule = namedtuple('Rule', ['rating', 'limit', 'is_upper_limit'])


def opposite(rule: Rule) -> Rule:
    return Rule(
        rating=rule.rating,
        limit=rule.limit-1 if rule.is_upper_limit else rule.limit+1,
        is_upper_limit=not rule.is_upper_limit)


def apply_rules(rules: list[Rule], ratings):
    new_ratings = dict(ratings)
    for rule in rules:
        old_lower, old_upper = new_ratings[rule.rating]
        new_range = (old_lower, min(rule.limit-1, old_upper)
                     ) if rule.is_upper_limit else (max(rule.limit+1, old_lower), old_upper)
        new_ratings[rule.rating] = new_range
    return new_ratings


def visit_workflow(workflow: str, workflow_moves: dict[str, dict], ratings):
    if workflow == 'A':
        return reduce(mul, (u-l+1 for l, u in ratings.values()))

    elif workflow == 'R':
        return 0

    total_num_combinations = 0
    for successor_workflow, all_rules in workflow_moves[workflow].items():
        for rules in all_rules:
            new_ratings = apply_rules(rules, ratings)
            total_num_combinations += visit_workflow(successor_workflow, workflow_moves, new_ratings)
    return total_num_combinations


def create_label(rules: list[Rule]):
    return '&'.join(f'{rule.rating}{"<" if rule.is_upper_limit else ">"}{rule.limit}'
                    for rule in rules)


def test():
    rule = Rule(
        rating='x',
        limit=500,
        is_upper_limit=False)

    ratings = {'x': (2166, 4000)}
    apply_rules([rule], ratings)


def main():
    filename = sys.argv[1]
    with open(filename) as workflows_and_parts_file:
        raw_workflows, raw_parts = tuple(p.splitlines() for p in workflows_and_parts_file.read().split('\n\n'))

    workflow_graph = pgv.AGraph(directed=True)
    workflow_moves = {}
    for raw_workflow in raw_workflows:
        name, raw_rules = WORKFLOW_PATTERN.search(raw_workflow).groups()
        workflow_moves[name] = defaultdict(list)
        previous_rules = []
        workflow_graph.add_node(name)

        for raw_rule in raw_rules.split(','):
            if (pattern_match := RULE_PATTERN.search(raw_rule)):
                rating, operator, limit, next_workflow = pattern_match.groups()

                rule = Rule(
                    rating=rating,
                    limit=int(limit),
                    is_upper_limit=operator == '<')

                # label = create_label([rule] + [opposite(r) for r in previous_rules])
                # workflow_graph.add_edge(name, next_workflow, label=label)

                rules = [rule] + [opposite(preceding_rule) for preceding_rule in previous_rules]
                workflow_moves[name][next_workflow].append(rules)

                previous_rules.append(rule)

            else:
                next_workflow = raw_rule
                rules = [opposite(preceding_rule) for preceding_rule in previous_rules]
                workflow_moves[name][next_workflow].append(rules)

                # label = create_label([opposite(r) for r in previous_rules])
                # workflow_graph.add_edge(name, raw_rule, label=label)

    # workflow_graph.layout(prog='dot')
    # workflow_graph.draw('graph.png')

    ratings = {
        'x': (1, 4000),
        'm': (1, 4000),
        'a': (1, 4000),
        's': (1, 4000)
    }

    num_combinations = visit_workflow('in', workflow_moves, ratings)
    print(num_combinations)


if __name__ == '__main__':
    test()
    main()
