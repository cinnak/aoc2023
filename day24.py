from aocd import get_data
from z3 import *

# 获取输入数据
data = get_data(year=2023, day=24).splitlines()

def is_parallel(v1, v2):
    # 检查两个速度向量是否平行
    cross_product = v1[0]*v2[1] - v1[1]*v2[0]
    return cross_product == 0

def find_intersection(p1, v1, p2, v2):
    # 计算两条轨迹的交点
    if is_parallel(v1, v2):
        return None
    
    x1, y1 = p1
    x2, y2 = p2
    vx1, vy1 = v1
    vx2, vy2 = v2
    
    # 求解参数方程
    s = (y2 - y1 - vy1*(x2-x1)/vx1) / (vy1*vx2/vx1 - vy2)
    t = (x2 + vx2*s - x1) / vx1
    
    # 检查是否在未来
    if t < 0 or s < 0:
        return None
    
    # 计算交点坐标
    x = x1 + vx1*t
    y = y1 + vy1*t
    
    return (x, y)

def is_in_test_area(point, min_coord, max_coord):
    # 检查点是否在测试区域内
    if point is None:
        return False
    x, y = point
    return min_coord <= x <= max_coord and min_coord <= y <= max_coord

def parse_line(line):
    # 解析输入数据行
    pos, vel = line.split('@')
    pos = tuple(map(int, pos.strip().split(',')))
    vel = tuple(map(int, vel.strip().split(',')))
    return (pos, vel)

def solve_pt1(hailstones, min_coord, max_coord):
    # 主解决函数
    count = 0
    n = len(hailstones)
    
    for i in range(n):
        for j in range(i + 1, n):
            p1 = hailstones[i][0][:2]
            v1 = hailstones[i][1][:2]
            p2 = hailstones[j][0][:2]
            v2 = hailstones[j][1][:2]
            
            intersection = find_intersection(p1, v1, p2, v2)
            if is_in_test_area(intersection, min_coord, max_coord):
                count += 1
    
    return count



def solve_part2(hailstones):
    solver = Solver()
    
    # 创建变量
    x = Int('x')
    y = Int('y')
    z = Int('z')
    vx = Int('vx')
    vy = Int('vy')
    vz = Int('vz')
    
    # 只需要前几个冰雹就足够确定解
    for i, (pos, vel) in enumerate(hailstones[:3]):
        t = Int(f't_{i}')
        solver.add(t >= 0)
        
        # 添加碰撞方程
        solver.add(x + vx * t == pos[0] + vel[0] * t)
        solver.add(y + vy * t == pos[1] + vel[1] * t)
        solver.add(z + vz * t == pos[2] + vel[2] * t)
    
    # 检查是否有解
    if solver.check() == sat:
        model = solver.model()
        # 获取初始位置坐标
        px = model[x].as_long()
        py = model[y].as_long()
        pz = model[z].as_long()
        return px + py + pz
    else:
        return "No solution found"




if __name__ == "__main__":
    data = get_data(year=2023, day=24).splitlines()
    hailstones = [parse_line(line) for line in data]
    # 设置测试区域范围
    MIN_COORD = 200000000000000
    MAX_COORD = 400000000000000

    # 计算结果
    result = solve_pt1(hailstones, MIN_COORD, MAX_COORD)
    print(f"在测试区域内相交的轨迹数量: {result}")

    print(f"初始位置坐标之和: {solve_part2(hailstones)}")