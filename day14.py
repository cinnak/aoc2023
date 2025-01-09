from aocd import get_data

def process_column_simple(col):
    total_load = 0
    height = len(col)
    
    # 用'#'分割列
    sections = col.split('#')
    current_pos = 0
    
    # 处理每个区域
    for section in sections:
        rocks = section.count('O')  # 区域内的石头数量
        # 计算这些石头的负载
        for i in range(rocks):
            load = height - (current_pos + i)
            total_load += load
        current_pos += len(section) + 1  # +1 是因为分割符'#'
        
    return total_load

def solve_simple(grid):
    total_load = 0
    width = len(grid[0])
    
    # 处理每一列
    for col_idx in range(width):
        col = get_column(grid, col_idx)
        total_load += process_column_simple(col)
        
    return total_load


"""part 2"""
def get_column(grid, col_index):
    return ''.join(row[col_index] for row in grid)

def calculate_load(grid):
    total_load = 0
    height = len(grid)
    for row_idx, row in enumerate(grid):
        rocks = row.count('O')
        load = (height - row_idx) * rocks
        total_load += load
    return total_load

def tilt(line):
    """在每个#之间，把O移到最前面"""
    parts = line.split('#')
    return '#'.join('O' * part.count('O') + '.' * part.count('.') for part in parts)

def get_cols(grid):
    """获取所有列"""
    return [''.join(row[i] for row in grid) for i in range(len(grid[0]))]

def tilt_north(grid):
    """向北滚动"""
    cols = get_cols(grid)
    new_cols = [tilt(col) for col in cols]
    return [''.join(col[i] for col in new_cols) for i in range(len(grid))]

def tilt_south(grid):
    """向南滚动"""
    cols = get_cols(grid)
    new_cols = [tilt(col[::-1])[::-1] for col in cols]
    return [''.join(col[i] for col in new_cols) for i in range(len(grid))]

def tilt_west(grid):
    """向西滚动"""
    return [tilt(row) for row in grid]

def tilt_east(grid):
    """向东滚动"""
    return [tilt(row[::-1])[::-1] for row in grid]

def cycle(grid):
    """一个完整的循环：北->西->南->东"""
    grid = tilt_north(grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    grid = tilt_east(grid)
    return grid

def solve(grid):
    seen = {}
    current = list(grid)
    
    for i in range(1000000000):
        state = '\n'.join(current)
        if state in seen:
            cycle_length = i - seen[state]
            remaining = (1000000000 - i) % cycle_length
            for _ in range(remaining):
                current = cycle(current)
            return current
        seen[state] = i
        current = cycle(current)
    return current






if __name__ == "__main__":
    data = get_data(year=2023, day=14).splitlines()

    print(f"Part 1: {solve_simple(data)}")
    print(f"Part 2: {calculate_load(solve(data))}")