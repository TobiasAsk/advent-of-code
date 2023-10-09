import sys


def do_job(job: str, jobs: dict):
    if job.isdigit():
        return int(job)

    first_monkey_name, operand, second_monkey_name = job.split()
    if operand == '+':
        return do_job(jobs[first_monkey_name], jobs) + do_job(jobs[second_monkey_name], jobs)
    elif operand == '-':
        return do_job(jobs[first_monkey_name], jobs) - do_job(jobs[second_monkey_name], jobs)
    elif operand == '*':
        return do_job(jobs[first_monkey_name], jobs) * do_job(jobs[second_monkey_name], jobs)
    elif operand == '/':
        return do_job(jobs[first_monkey_name], jobs) // do_job(jobs[second_monkey_name], jobs)


def expand_in_postfix(expression: str, jobs: dict):
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

def main():
    filename = sys.argv[1]
    jobs = {}
    with open(filename) as job_list:
        for line in job_list:
            monkey_name, job = line.split(':')
            jobs[monkey_name] = job.strip()
    result = do_job(jobs['root'], jobs)
    print(result)


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
    a = 3

if __name__ == '__main__':
    test()
    main()
