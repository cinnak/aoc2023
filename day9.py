
from aocd import get_data

def data_process():
    data = get_data(year=2023, day=9).splitlines()
    data = [list(map(int, line.split())) for line in data]
    return data

def calc_next_pt1(numbers):
    diff = [numbers[i] - numbers[i-1] for i in range(1, len(numbers))]
    if not all(x==0 for x in diff):
        next_diff = calc_next_pt1(diff)
        return numbers[-1] + next_diff
    return numbers[-1]

def solve_pt1(data):
    return sum(calc_next_pt1(numbers) for numbers in data)

def calc_next_pt2(numbers):
    diff = [numbers[i] - numbers[i-1] for i in range(1, len(numbers))]
    if not all(x==0 for x in diff):
        next_diff = calc_next_pt2(diff)
        return numbers[0] - next_diff
    return numbers[0]

def solve_pt2(data):
    return sum(calc_next_pt2(numbers) for numbers in data)

if __name__ == "__main__":
    data = data_process()
    print(solve_pt1(data))
    print(solve_pt2(data))
