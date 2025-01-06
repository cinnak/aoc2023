from multiprocessing import Pool
import os
from aocd import get_data

def pack_state(pos, used_numbers, current_group):
    """将三个状态值打包成一个整数"""
    return (pos << 16) | (used_numbers << 8) | current_group

def is_valid_end(used_numbers, current_group, numbers):
    """检查结束位置是否合法"""
    if current_group > 0:
        return (used_numbers == len(numbers) - 1 and 
                current_group == numbers[used_numbers])
    return used_numbers == len(numbers)

def can_finish_remaining(pos, used_numbers, current_group, pattern, numbers):
    """检查剩余空间是否足够"""
    remaining_space = len(pattern) - pos
    remaining_numbers = numbers[used_numbers:]
    
    if current_group > 0:
        if used_numbers >= len(numbers) or current_group > numbers[used_numbers]:
            return False
        remaining_numbers = numbers[used_numbers + 1:]
    
    min_space_needed = sum(remaining_numbers) + len(remaining_numbers) - 1
    return remaining_space >= min_space_needed

class SpringSolver:
    def __init__(self):
        self.cache = {}

    def count_arrangements(self, pos, used_numbers, current_group, pattern, numbers):
        """计算可能的排列数量"""
        # 提前返回检查
        if not can_finish_remaining(pos, used_numbers, current_group, pattern, numbers):
            return 0

        if pos == len(pattern):
            return 1 if is_valid_end(used_numbers, current_group, numbers) else 0

        # 使用打包的状态作为缓存键
        state = pack_state(pos, used_numbers, current_group)
        if state in self.cache:
            return self.cache[state]

        result = 0
        chars = ['.', '#'] if pattern[pos] == '?' else [pattern[pos]]

        for c in chars:
            if c == '.':
                if current_group == 0:
                    result += self.count_arrangements(pos + 1, used_numbers, 0, pattern, numbers)
                elif used_numbers < len(numbers) and current_group == numbers[used_numbers]:
                    result += self.count_arrangements(pos + 1, used_numbers + 1, 0, pattern, numbers)
            else:  # c == '#'
                if used_numbers < len(numbers) and current_group < numbers[used_numbers]:
                    result += self.count_arrangements(pos + 1, used_numbers, current_group + 1, pattern, numbers)

        self.cache[state] = result
        return result

    def solve_line(self, line):
        """解决单行输入"""
        pattern, numbers = line.split()
        numbers = [int(x) for x in numbers.split(',')]
        self.cache = {}
        return self.count_arrangements(0, 0, 0, pattern, numbers)

def parallel_solve(data, num_processes=None):
    """并行处理所有输入行"""
    if num_processes is None:
        num_processes = os.cpu_count()

    with Pool(num_processes) as pool:
        solver = SpringSolver()
        results = pool.map(solver.solve_line, data)

    return sum(results)

def unfold_line(line):
    """将一行数据展开5倍"""
    pattern, numbers = line.split()
    # 用?连接pattern重复5次
    new_pattern = '?'.join([pattern] * 5)
    # 重复numbers 5次
    numbers = [int(x) for x in numbers.split(',')]
    new_numbers = numbers * 5
    return f"{new_pattern} {','.join(map(str, new_numbers))}"
def solve_part2(data):
    """解决第二部分"""
    # 展开数据
    unfolded_data = [unfold_line(line) for line in data]
    # 使用之前的并行解决方案
    return parallel_solve(unfolded_data)

if __name__ == '__main__':
    data = get_data(year=2023, day=12).splitlines()
    print(f"使用 {os.cpu_count()} 个进程并行计算中...")
    result = parallel_solve(data)
    print(f"结果是: {result}")
    pt2_result = solve_part2(data)
    print(f"结果是: {pt2_result}")
