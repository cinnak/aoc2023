from aocd import get_data

def gcd(a, b):
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return a

def track_path(instructions):
    """根据指令追踪路径，返回顶点列表"""
    x, y = 0, 0
    vertices = [(x, y)]
    
    directions = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1)
    }
    
    for line in instructions.split('\n'):
        if not line.strip():
            continue
        direction, steps, _ = line.split()
        steps = int(steps)
        dx, dy = directions[direction]
        x += dx * steps
        y += dy * steps
        vertices.append((x, y))
    
    return vertices

def calculate_area(vertices):
    """使用鞋带公式计算多边形面积"""
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[i][1] * vertices[j][0]
    return abs(area) / 2

def count_boundary_points(vertices):
    """计算边界上的点数量"""
    boundary_points = 0
    n = len(vertices)
    for i in range(n):
        j = (i + 1) % n
        dx = abs(vertices[j][0] - vertices[i][0])
        dy = abs(vertices[j][1] - vertices[i][1])
        boundary_points += gcd(dx, dy)
    return boundary_points

def solve_part1(data):
    """解决第一部分问题"""
    # 获取顶点
    vertices = track_path(data)
    
    # 计算面积
    area = calculate_area(vertices)
    
    # 计算边界点数量
    boundary_points = count_boundary_points(vertices)
    
    # 使用Pick定理计算内部点数量
    interior_points = int(area - boundary_points/2 + 1)
    
    # 计算总体积
    total_volume = interior_points + boundary_points
    
    return total_volume

"""part2"""
def parse_hex_instruction(hex_code):
    """从十六进制代码解析真实指令"""
    # 去掉'#'号
    hex_code = hex_code.strip('(#)')
    
    # 前5位是距离
    distance = int(hex_code[:5], 16)
    
    # 最后一位是方向
    direction_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    direction = direction_map[hex_code[5]]
    
    return direction, distance

def track_path_part2(instructions):
    """处理Part 2的路径追踪"""
    x = y = 0
    vertices = [(x, y)]
    
    for line in instructions.strip().split('\n'):
        # 提取十六进制代码
        hex_code = line.split()[-1]
        direction, steps = parse_hex_instruction(hex_code)
        
        # 其余逻辑与Part 1相同
        if direction == 'R': x += steps
        elif direction == 'L': x -= steps
        elif direction == 'U': y += steps
        else: y -= steps
        
        vertices.append((x, y))
    
    return vertices

def solve_part2(instructions):
    """Part 2的完整解决方案"""
    x = y = area = boundary = 0
    
    for line in instructions.strip().split('\n'):
        # 解析十六进制指令
        hex_code = line.split()[-1].strip('(#)')
        distance = int(hex_code[:5], 16)
        direction = {'0':'R', '1':'D', '2':'L', '3':'U'}[hex_code[5]]
        
        # 计算新坐标
        new_x, new_y = x, y
        if direction == 'R': new_x += distance
        elif direction == 'L': new_x -= distance
        elif direction == 'U': new_y += distance
        else: new_y -= distance
        
        # 计算面积和边界
        area += x * new_y - new_x * y
        boundary += abs(new_x - x + new_y - y)
        
        x, y = new_x, new_y
    
    # 使用Pick定理计算总体积
    return int(abs(area) / 2) + boundary // 2 + 1









if __name__ == "__main__":
    data = get_data(year=2023, day=18)
    result_pt1 = solve_part1(data)
    print(f"Part 1答案：熔岩池可以容纳 {result_pt1} 立方米的熔岩")
    result_pt2 = solve_part2(data)
    print(f"Part 2答案：熔岩池可以容纳 {result_pt2} 立方米的熔岩")