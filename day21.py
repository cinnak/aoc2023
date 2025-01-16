from aocd import get_data
import numpy as np

def solve_part1_correct(data, steps=64):
    # 1. 正确处理输入数据
    rows = len(data)
    grid = np.zeros((rows, rows), dtype=int)
    start = None
    
    # 找到S并正确设置地图
    for i in range(rows):
        for j in range(rows):
            if data[i][j] == '#':
                grid[i][j] = 1
            elif data[i][j] == 'S':
                start = (i, j)
    
    # 2. BFS从S开始
    positions = {start}
    for _ in range(steps):
        positions = {
            (ny, nx)
            for y, x in positions
            for ny, nx in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]
            if 0 <= ny < rows and 0 <= nx < rows and grid[ny][nx] == 0
        }
    
    return len(positions)





def solve_part2_simple(grid, total_steps):
    size = len(grid)
    # 只需计算三个关键点：65, 196, 327步
    points = []
    for i in range(3):
        steps = 65 + i * 131
        positions = {(65, 65)}  # 起始位置
        for _ in range(steps):
            next_pos = set()
            for y, x in positions:
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if grid[ny % size][nx % size] == 0:
                        next_pos.add((ny, nx))
            positions = next_pos
        points.append(len(positions))
    
    # 用三个点计算二次函数
    n = total_steps // size
    a = points[0]
    b = points[1] - points[0]
    c = points[2] - 2*points[1] + points[0]
    return a + b*n + (c//2)*n*(n-1)


if __name__ == "__main__":
    data = get_data(year=2023, day=21).splitlines()
    grid = np.array([[1 if c == '#' else 0 for c in row] for row in data])
    print(f'part1: {solve_part1_correct(data)}')
    print(f'part2: {solve_part2_simple(grid, total_steps = 26501365)}')
