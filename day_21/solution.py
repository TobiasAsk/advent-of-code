import sys
from dataclasses import dataclass

OPERATORS = ['+', '*', '/', '-', '=']
INVERSIONS = {
    '+': '-',
    '-': '+',
    '/': '*',
    '*': '/'
}


def expand_in_postfix(expression: str, jobs: dict) -> str:
    lhs, _, rhs = expression.split()
    expr = [lhs, rhs, '=']
    while True:
        new_symbols = []
        for symbol in expr:
            expanded = jobs.get(symbol, symbol)
            parts = expanded.split()
            if len(parts) > 1:
                operand, operator, other_operand = parts
                new_symbols.extend([operand, other_operand, operator])
            else:
                new_symbols.append(expanded)
        if new_symbols == expr:
            break
        expr = list(new_symbols)
    return str.join(' ', expr)


@dataclass
class Node:

    value: str
    left_operand: None = None
    right_operand: None = None

    def is_operator(self) -> bool:
        return self.value in OPERATORS


def build_tree(postfix: str) -> Node:
    stack = []
    operators = ['+', '*', '/', '-', '=']
    for symbol in postfix.split():
        if symbol in operators:
            second_operand = stack.pop()
            first_operand = stack.pop()
            operator_node = Node(
                value=symbol,
                left_operand=first_operand,
                right_operand=second_operand)
            stack.append(operator_node)
        else:
            stack.append(Node(symbol))
    return stack.pop()


def apply_inverted_operation(root: Node, operator: Node):
    new_subtree_root: Node = (operator.left_operand if operator.left_operand.is_operator()
                              else operator.right_operand)
    root.left_operand = new_subtree_root
    operator.value = INVERSIONS[operator.value]
    operand = (operator.left_operand if not operator.left_operand.is_operator()
               else operator.right_operand)

    new_subtree_rhs = root.right_operand
    root.right_operand = operator
    operator.left_operand = new_subtree_rhs
    operator.right_operand = operand


def main():
    filename = sys.argv[1]
    jobs = {}
    with open(filename) as job_list:
        for line in job_list:
            monkey_name, job = line.split(':')
            jobs[monkey_name] = job.strip()
    jobs['humn'] = 'humn'
    postfix = expand_in_postfix(jobs['root'], jobs)
    tree = build_tree(postfix)
    g = 2


def test():
    jobs = {
        'root': 'a = b',
        'a': 'c * d',
        'b': '3',
        'c': '2',
        'd': 'e + f',
        'e': '1',
        'f': '1'
    }
    postfix = expand_in_postfix(jobs['root'], jobs)
    tree = build_tree('2 3 X + * 10 =')
    while not tree.left_operand.value == 'X':
        apply_inverted_operation(tree, tree.left_operand)
    a = 2



if __name__ == '__main__':
    test()
    main()
