from collections import defaultdict
from heapq import heappush, heappop
from aocd import get_data

# 定义方向常量：右、下、左、上
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def get_next_directions(current_dir, steps):
    # 如果还没走满3步，可以继续当前方向
    if steps < 3:
        yield current_dir
    
    # 总是可以左转和右转
    # 左转：当前方向-1，如果小于0则变为3
    yield (current_dir - 1) % 4
    # 右转：当前方向+1，如果大于3则变为0
    yield (current_dir + 1) % 4

def min_heat_loss(grid):
    grid = [[int(c) for c in line] for line in grid.split('\n')]
    rows, cols = len(grid), len(grid[0])
    
    queue = [(0, 0, 0, 0, 0)]  # (热量损失, x, y, 方向, 连续步数)
    seen = set()
    
    while queue:
        heat, x, y, direction, steps = heappop(queue)
        
        # 到达终点
        if x == rows-1 and y == cols-1:
            return heat
            
        # 获取下一步可能的方向
        for new_dir in get_next_directions(direction, steps):
            # 计算新位置
            new_steps = 1 if new_dir != direction else steps + 1
            new_x = x + DIRS[new_dir][0]
            new_y = y + DIRS[new_dir][1]
            
            # 检查是否有效
            if not (0 <= new_x < rows and 0 <= new_y < cols):
                continue
                
            # 状态去重
            state = (new_x, new_y, new_dir, new_steps)
            if state in seen:
                continue
            seen.add(state)
            
            # 计算新的热量损失并加入队列
            new_heat = heat + grid[new_x][new_y]
            heappush(queue, (new_heat, new_x, new_y, new_dir, new_steps))

"""part 2"""
def get_next_directions_pt2(current_dir, steps):
    # 如果步数小于4，只能继续直走
    if steps < 4:
        yield current_dir
    # 如果步数在4到10之间，可以继续直走或转向
    elif 4 <= steps <= 10:
        # 可以左转和右转
        yield (current_dir - 1) % 4
        yield (current_dir + 1) % 4
        # 也可以继续直走
        if steps < 10:
            yield current_dir
    # 如果已经走了10步，必须转向
    else:  # steps == 10
        yield (current_dir - 1) % 4
        yield (current_dir + 1) % 4

def min_heat_loss_pt2(grid):
    grid = [[int(c) for c in line] for line in grid.split('\n')]
    rows, cols = len(grid), len(grid[0])
    
    # 初始状态：可以向右或向下开始
    queue = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]  # (热量损失, x, y, 方向, 连续步数)
    seen = set()
    
    while queue:
        heat, x, y, direction, steps = heappop(queue)
        
        # 到达终点且至少走了4步
        if x == rows-1 and y == cols-1 and steps >= 4:
            return heat
            
        # 获取下一步可能的方向
        for new_dir in get_next_directions_pt2(direction, steps):
            new_steps = 1 if new_dir != direction else steps + 1
            new_x = x + DIRS[new_dir][0]
            new_y = y + DIRS[new_dir][1]
            
            # 检查是否有效
            if not (0 <= new_x < rows and 0 <= new_y < cols):
                continue
                
            # 状态去重
            state = (new_x, new_y, new_dir, new_steps)
            if state in seen:
                continue
            seen.add(state)
            
            # 计算新的热量损失并加入队列
            new_heat = heat + grid[new_x][new_y]
            heappush(queue, (new_heat, new_x, new_y, new_dir, new_steps))


if __name__ == "__main__":
    data = get_data(year=2023, day=17)
    result_pt1 = min_heat_loss(data)
    print(f'pt1: {result_pt1}')
    result_pt2 = min_heat_loss_pt2(data)
    print(f'pt2: {result_pt2}')