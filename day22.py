from aocd import get_data

class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def get_all_points(self):
        points = []
        x1, y1, z1 = self.start
        x2, y2, z2 = self.end
        
        # 确定哪个维度有变化
        if x1 != x2:
            # x方向的直线
            for x in range(min(x1, x2), max(x1, x2) + 1):
                points.append((x, y1, z1))
        elif y1 != y2:
            # y方向的直线
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points.append((x1, y, z1))
        else:
            # z方向的直线
            for z in range(min(z1, z2), max(z1, z2) + 1):
                points.append((x1, y1, z))
        return points
    
    def get_min_z(self):
        return min(self.start[2], self.end[2])
    
    def move_down(self, distance):
        x1, y1, z1 = self.start
        x2, y2, z2 = self.end
        self.start = (x1, y1, z1 - distance)
        self.end = (x2, y2, z2 - distance)
    
    def can_move_down(self, occupied_points):
        current_points = self.get_all_points()
        for x, y, z in current_points:
            if z == 1:  # 已经到达地面
                return False
            if (x, y, z - 1) in occupied_points:
                return False
        return True
    
    def __repr__(self):
        return f"Brick({self.start}, {self.end})"

def parse_input(data):
    bricks = []
    for line in data:
        start_str, end_str = line.split('~')
        start = tuple(map(int, start_str.split(',')))
        end = tuple(map(int, end_str.split(',')))
        bricks.append(Brick(start, end))
    return bricks

def sort_bricks(bricks):
    return sorted(bricks, key=lambda brick: brick.get_min_z())

def simulate_falling(bricks):
    sorted_bricks = sort_bricks(bricks)
    occupied_points = set()
    point_to_brick = {}
    supports = {brick: set() for brick in bricks}
    supported_by = {brick: set() for brick in bricks}
    
    for brick in sorted_bricks:
        while brick.can_move_down(occupied_points):
            brick.move_down(1)
            
        current_points = brick.get_all_points()
        for point in current_points:
            point_to_brick[point] = brick
            
        for x, y, z in current_points:
            below_point = (x, y, z-1)
            if below_point in occupied_points:
                supporting_brick = point_to_brick[below_point]
                supported_by[brick].add(supporting_brick)
                supports[supporting_brick].add(brick)
                
        occupied_points.update(current_points)
    
    return supports, supported_by
def can_safely_disintegrate(brick, supports, supported_by):
    """判断一个砖块是否可以安全移除"""
    # 检查这个砖块支撑的所有砖块
    for supported_brick in supports[brick]:
        # 如果有任何一个被支撑的砖块只有这一个支撑，则不能移除
        if len(supported_by[supported_brick]) == 1:
            return False
    return True

def count_safely_removable(bricks, supports, supported_by):
    """计算可以安全移除的砖块数量"""
    count = 0
    for brick in bricks:
        if can_safely_disintegrate(brick, supports, supported_by):
            count += 1
    return count
def solve_part1(data):
    # 解析输入
    bricks = parse_input(data)
    
    # 模拟砖块下落
    supports, supported_by = simulate_falling(bricks)
    
    # 计算可以安全移除的砖块数量
    return count_safely_removable(bricks, supports, supported_by)
"""part 2"""
def count_falling_bricks(brick, supports, supported_by):
    """计算移除一个砖块后会掉落的其他砖块数量"""
    falling = set()  # 记录会掉落的砖块
    queue = [brick]  # 用于广度优先搜索的队列
    
    # 使用广度优先搜索找出所有会掉落的砖块
    while queue:
        current = queue.pop(0)
        # 检查当前砖块支撑的所有砖块
        for supported_brick in supports[current]:
            # 如果这个砖块还没被标记为掉落
            if supported_brick not in falling:
                # 检查支撑它的砖块是否都会掉落
                supporting_bricks = supported_by[supported_brick]
                if all(b == brick or b in falling for b in supporting_bricks):
                    falling.add(supported_brick)
                    queue.append(supported_brick)
    
    return len(falling)  # 返回掉落的砖块数量

def solve_part2(data):
    # 解析输入
    bricks = parse_input(data)
    
    # 模拟砖块下落
    supports, supported_by = simulate_falling(bricks)
    
    # 计算每个砖块被移除后导致的掉落数量总和
    total_falling = 0
    for brick in bricks:
        falling_count = count_falling_bricks(brick, supports, supported_by)
        total_falling += falling_count
    
    return total_falling


if __name__ == "__main__":
    data = get_data(year=2023, day=22).splitlines()
    result_pt1 = solve_part1(data)
    print(f"Part 1 答案: {result_pt1}")
    result_pt2 = solve_part2(data)
    print(f"Part 2 答案: {result_pt2}")
