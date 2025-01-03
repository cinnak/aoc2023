from aocd import get_data

# 定义管道类型和连接方向
pipes = {
    '|': {'N', 'S'},  # 竖直管道：连接上下
    '-': {'E', 'W'},  # 水平管道：连接左右
    'L': {'N', 'E'},  # 左下弯管：连接上右
    'J': {'N', 'W'},  # 右下弯管：连接上左
    '7': {'S', 'W'},  # 右上弯管：连接下左
    'F': {'S', 'E'},  # 左上弯管：连接下右
}

# 定义方向和对应的位置变化
directions = {
    'N': (-1, 0),   # 上：行号-1
    'S': (1, 0),    # 下：行号+1
    'W': (0, -1),   # 左：列号-1
    'E': (0, 1)     # 右：列号+1
}

# 用于管道方向映射
pipe_turns = {
    'L': {'S': 'E', 'N': 'E'},
    'J': {'S': 'W', 'N': 'W'},
    '7': {'N': 'W', 'S': 'S'},
    'F': {'N': 'E', 'S': 'E'}
}

def is_valid_position(row, col, grid):
    """检查位置是否在网格范围内"""
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def can_connect(pipe, my_direction, their_direction):
    """检查管道是否可以连接"""
    return their_direction in pipes.get(pipe, {})

def get_next_pos(pos, direction, grid):
    """获取下一个位置和新的方向"""
    row, col = pos
    dr, dc = directions[direction]
    next_row, next_col = row + dr, col + dc
    
    if not is_valid_position(next_row, next_col, grid):
        return None, None  # 无效位置
    
    pipe = grid[next_row][next_col]
    next_direction = direction
    
    if pipe in pipe_turns:
        next_direction = pipe_turns[pipe].get(direction, direction)
    
    return (next_row, next_col), next_direction

def trace_loop(start_pos, grid):
    """追踪整个循环，返回每个点的距离"""
    visited = set()  # 用于记录已访问的节点
    path = []
    current_pos = start_pos
    current_direction = 'N'  # 起始方向是任意的，假设从北开始
    
    # 先找到完整的路径
    while current_pos not in visited:
        visited.add(current_pos)
        path.append(current_pos)
        
        next_pos, next_direction = get_next_pos(current_pos, current_direction, grid)
        
        if next_pos is None:
            break
        
        current_pos = next_pos
        current_direction = next_direction
    
    # 计算每个点的最短距离
    total_steps = len(path)
    distances = {}
    for i, pos in enumerate(path):
        clockwise = i
        counterclockwise = total_steps - i
        distances[pos] = min(clockwise, counterclockwise)
    
    return distances

if __name__ == "__main__":
    data = get_data(year=2023, day=10)
    data = data.splitlines()

    # 找到起点S
    start = None
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == 'S':
                start = (i, j)
                break
        if start:
            break

    print(f"找到起点位置: {start}")

    # 计算最远距离
    distances = trace_loop(start, data)
    max_distance = max(distances.values())
    print(f"最远的点距离为: {max_distance}")

    # 找出最远的点
    farthest_points = [pos for pos, dist in distances.items() if dist == max_distance]
    print(f"最远的点的位置: {farthest_points}")
