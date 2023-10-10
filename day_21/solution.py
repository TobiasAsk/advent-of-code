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


def apply_inverted_operation(root: Node, operator: Node, keep_left):
    new_subtree_root = operator.left_operand if keep_left else operator.right_operand
    root.left_operand = new_subtree_root
    operator.value = INVERSIONS[operator.value]
    operand = operator.right_operand if keep_left else operator.left_operand

    new_subtree_rhs = root.right_operand
    root.right_operand = operator
    operator.left_operand = new_subtree_rhs
    operator.right_operand = operand


def main():
    filename = sys.argv[1]
    jobs: dict[str, str] = {}
    with open(filename) as job_list:
        for line in job_list:
            monkey_name, job = line.split(':')
            jobs[monkey_name] = job.strip()
    jobs['humn'] = 'humn'
    jobs['root'] = jobs['root'].replace('+', '=')
    postfix = expand_in_postfix(jobs['root'], jobs)
    tree = build_tree(postfix)
    path = search('humn', tree)
    for operator, pick_right_child in path[1:-1]:
        apply_inverted_operation(tree, operator, pick_right_child)
    solution = solve(tree.right_operand)
    print(solution)


def solve(subtree: Node):
    if not subtree.is_operator():
        return int(subtree.value)
    left_operand = solve(subtree.left_operand)
    right_operand = solve(subtree.right_operand)
    if subtree.value == '/':
        return left_operand // right_operand
    elif subtree.value == '-':
        return left_operand - right_operand
    elif subtree.value == '+':
        return left_operand + right_operand
    elif subtree.value == '*':
        return left_operand * right_operand

def search(target: str, node: Node):
    if node.value == target:
        return [(node, None)]
    first_option = search(target, node.left_operand) if node.left_operand else None
    if first_option:
        return [(node, True)] + first_option
    second_option = search(target, node.right_operand) if node.right_operand else None
    if second_option: return [(node, False)] + second_option
    return None

def test():
    tree = build_tree('2 1 + 3 X + * 12 =')
    path = search('X', tree)
    for operator, pick_right_child in path[1:-1]:
        apply_inverted_operation(tree, operator, pick_right_child)
    solution = solve(tree.right_operand)
    assert solution == 1


if __name__ == '__main__':
    # test()
    main()
