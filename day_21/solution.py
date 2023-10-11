import sys


def do_job(job: str, jobs: dict):
    if job.isdigit():
        return int(job)

    first_monkey_name, operator, second_monkey_name = job.split()
    if operator == '+':
        return do_job(jobs[first_monkey_name], jobs) + do_job(jobs[second_monkey_name], jobs)
    elif operator == '-':
        return do_job(jobs[first_monkey_name], jobs) - do_job(jobs[second_monkey_name], jobs)
    elif operator == '*':
        return do_job(jobs[first_monkey_name], jobs) * do_job(jobs[second_monkey_name], jobs)
    elif operator == '/':
        return do_job(jobs[first_monkey_name], jobs) / do_job(jobs[second_monkey_name], jobs)
    elif operator == '=':
        left_operand = do_job(jobs[first_monkey_name], jobs)
        right_operand = do_job(jobs[second_monkey_name], jobs)
        if left_operand == right_operand:
            return 'Eureka'
        return left_operand > right_operand


def search(lower_limit: int, upper_limit: int, jobs: dict[str, str]):
    value = (upper_limit + lower_limit) / 2
    jobs['humn'] = str(int(value))
    is_higher = do_job(jobs['root'], jobs)
    if is_higher == 'Eureka':
        return value
    if is_higher:
        return search(value, upper_limit, jobs)
    else:
        return search(lower_limit, value, jobs)


def main():
    filename = sys.argv[1]
    jobs: dict[str, str] = {}
    with open(filename) as job_list:
        for line in job_list:
            monkey_name, job = line.split(':')
            jobs[monkey_name] = job.strip()
    jobs['root'] = jobs['root'].replace('+', '=')
    lower_limit = None
    while True:
        left_side_higher = do_job(jobs['root'], jobs)
        if left_side_higher:
            lower_limit = jobs['humn']
            jobs['humn'] = str(int(jobs['humn']) * 2)
        else:
            break

    upper_limit = jobs['humn']
    value = search(int(lower_limit), int(upper_limit), jobs)
    print(value)


if __name__ == '__main__':
    main()
