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
        'f': '5',
        'g': '3'
    }
    result = do_job('f + g', jobs)
    print(f'Result is {result}')


if __name__ == '__main__':
    main()
