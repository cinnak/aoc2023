from aocd import get_data
import networkx as nx



def get_next_positions(row, col, grid, visited):
    next_positions = []
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    
    current = grid[row][col]
    if current in '^v<>':
        dr, dc = directions[current]
        next_row, next_col = row + dr, col + dc
        if (0 <= next_row < len(grid) and 
            0 <= next_col < len(grid[0]) and 
            grid[next_row][next_col] != '#' and 
            (next_row, next_col) not in visited):
            next_positions.append((next_row, next_col))
    else:
        for dr, dc in directions.values():
            next_row, next_col = row + dr, col + dc
            if (0 <= next_row < len(grid) and 
                0 <= next_col < len(grid[0]) and 
                grid[next_row][next_col] != '#' and 
                (next_row, next_col) not in visited):
                next_positions.append((next_row, next_col))
    
    return next_positions

def dfs_iterative(start_row, start_col, grid, end_pos):
    stack = [(start_row, start_col, 0)]  # 添加路径长度到栈中
    visited = set()
    visited.add((start_row, start_col))

    while stack:
        row, col, length = stack.pop()  # 解包路径长度
        if (row, col) == end_pos:
            return length  # 返回到达目标时的路径长度
        
        next_positions = get_next_positions(row, col, grid, visited)
        for next_row, next_col in next_positions:
            if (next_row, next_col) not in visited:
                visited.add((next_row, next_col))
                stack.append((next_row, next_col, length + 1))  # 更新路径长度
                # visited.remove((next_row, next_col))  # 不需要在这里移除，栈会管理

    return float('-inf')  # 如果没有找到路径

def find_longest_path(grid):
    start_col = grid[0].index('.')
    end_col = grid[-1].index('.')
    start_pos = (0, start_col)
    end_pos = (len(grid)-1, end_col)
    
    return dfs_iterative(start_pos[0], start_pos[1], grid, end_pos)

"""part2"""
def find_junctions(grid):
    """使用列表推导式找出分叉点"""
    rows, cols = len(grid), len(grid[0])
    start = (0, grid[0].index('.'))
    end = (rows-1, grid[-1].index('.'))
    
    def count_neighbors(r, c):
        return sum(0 <= r+dr < rows and 0 <= c+dc < cols and grid[r+dr][c+dc] != '#'
                  for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)])
    
    junctions = {start, end} | {
        (r, c) 
        for r in range(rows) 
        for c in range(cols)
        if grid[r][c] != '#' and count_neighbors(r, c) > 2
    }
    
    return junctions

def build_graph_nx(grid):
    """构建压缩后的图"""
    junctions = find_junctions(grid)
    G = nx.Graph()
    
    def explore_path(start, curr_pos, curr_dist, visited):
        r, c = curr_pos
        if curr_pos in junctions and curr_pos != start and curr_dist > 0:
            G.add_edge(start, curr_pos, weight=curr_dist)
            return
            
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            next_pos = (nr, nc)
            if (0 <= nr < len(grid) and 
                0 <= nc < len(grid[0]) and 
                grid[nr][nc] != '#' and 
                next_pos not in visited):
                visited.add(next_pos)
                explore_path(start, next_pos, curr_dist + 1, visited)
                visited.remove(next_pos)
    
    for junction in junctions:
        visited = {junction}
        explore_path(junction, junction, 0, visited)
    
    return G, junctions

def find_longest_path_nx(G, start, end):
    """在压缩后的图中寻找最长路径"""
    def dfs_longest_path(current, visited, length):
        if current == end:
            return length
            
        max_length = float('-inf')
        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path_length = dfs_longest_path(neighbor, 
                                            visited, 
                                            length + G[current][neighbor]['weight'])
                visited.remove(neighbor)
                max_length = max(max_length, path_length)
                
        return max_length
    
    return dfs_longest_path(start, {start}, 0)

def solve_part2_nx(grid):
    """解决Part 2"""
    # 构建图
    G, _ = build_graph_nx(grid)
    
    # 确定起点和终点
    start = (0, grid[0].index('.'))
    end = (len(grid)-1, grid[-1].index('.'))
    
    # 寻找最长路径
    return find_longest_path_nx(G, start, end)

if __name__ == "__main__":
    data = get_data(year=2023, day=23).splitlines()
    grid = [list(row) for row in data]
    print("Part 1 答案：:", find_longest_path(grid))
    print(f"Part 2 最长路径长度: {solve_part2_nx(grid)}")

    