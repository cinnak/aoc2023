from itertools import product
from aocd import get_data

def parse_line(line):
    pattern, group_str  = line.split()
    groups  = [int(x) for x in group_str.split(',')]
    return pattern, groups  

def generate_combinations(pattern):
    options = [(c if c != '?' else ['.', '#']) for c in pattern]
    return product(*options)

def validate_groups(spring, groups):
    # 统计连续 # 的分组大小
    sizes = [len(g) for g in ''.join(spring).split('.') if g]
    return sizes == groups

def count_valid_arrangements(pattern, groups):
    valid_count = 0
    for arrangement in generate_combinations(pattern):
        if validate_groups(arrangement, groups):
            valid_count += 1
    return valid_count  
    
def solve_pt1(data):
    total = 0
    for line in data:
        pattern, groups = parse_line(line)
        total += count_valid_arrangements(pattern, groups)
    return total







    
if __name__ == '__main__':
    data = get_data(year=2023, day=12).splitlines()
    print(solve_pt1(data))