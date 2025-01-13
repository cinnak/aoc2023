from aocd import get_data



def simulate_beam_simple(grid):
    # 用元组存储状态：(x, y, dx, dy)
    beams = [(0, 0, 0, 1)]  # 起始位置和方向
    visited = set()  # 记录已访问的状态
    energized = set()  # 记录被充能的位置
    
    while beams:
        x, y, dx, dy = beams.pop(0)
        
        # 检查是否越界或重复
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])) or (x, y, dx, dy) in visited:
            continue
            
        visited.add((x, y, dx, dy))
        energized.add((x, y))
        
        # 获取当前格子
        cell = grid[x][y]
        
        # 处理不同类型的格子
        if cell == '.' or (cell == '|' and dy == 0) or (cell == '-' and dx == 0):
            beams.append((x + dx, y + dy, dx, dy))
        elif cell == '/':
            beams.append((x - dy, y - dx, -dy, -dx))
        elif cell == '\\':
            beams.append((x + dy, y + dx, dy, dx))
        elif cell == '|' and dy != 0:
            beams.extend([(x - 1, y, -1, 0), (x + 1, y, 1, 0)])
        elif cell == '-' and dx != 0:
            beams.extend([(x, y - 1, 0, -1), (x, y + 1, 0, 1)])
            
    return len(energized)

"""part 2"""


def simulate_beam_with_start(grid, start_x, start_y, start_dx, start_dy):
    beams = [(start_x, start_y, start_dx, start_dy)]
    visited = set()
    energized = set()
    
    while beams:
        x, y, dx, dy = beams.pop(0)
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])) or (x, y, dx, dy) in visited:
            continue
        visited.add((x, y, dx, dy))
        energized.add((x, y))
        
        cell = grid[x][y]
        if cell == '.' or (cell == '|' and dy == 0) or (cell == '-' and dx == 0):
            beams.append((x + dx, y + dy, dx, dy))
        elif cell == '/':
            beams.append((x - dy, y - dx, -dy, -dx))
        elif cell == '\\':
            beams.append((x + dy, y + dx, dy, dx))
        elif cell == '|' and dy != 0:
            beams.extend([(x - 1, y, -1, 0), (x + 1, y, 1, 0)])
        elif cell == '-' and dx != 0:
            beams.extend([(x, y - 1, 0, -1), (x, y + 1, 0, 1)])
            
    return len(energized)

def find_max_energized_simple(grid):
    rows, cols = len(grid), len(grid[0])
    
    # 所有可能的起始位置和方向
    starts = (
        [(0, y, 1, 0) for y in range(cols)] +          # 顶部向下
        [(rows-1, y, -1, 0) for y in range(cols)] +    # 底部向上
        [(x, 0, 0, 1) for x in range(rows)] +          # 左边向右
        [(x, cols-1, 0, -1) for x in range(rows)]      # 右边向左
    )
    
    return max(simulate_beam_with_start(grid, x, y, dx, dy) 
              for x, y, dx, dy in starts)


if __name__ == "__main__":
    # 获取输入数据
    data = get_data(year=2023, day=16).splitlines()
    # 转换输入数据为二维列表
    grid = [list(row) for row in data]

    # 运行并打印结果
    result = simulate_beam_simple(grid)
    print(f"Part 1答案：{result}")


    result_pt2 = find_max_energized_simple(grid)
    print(f"Part 2答案：{result_pt2}")
