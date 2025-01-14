from aocd import get_data


def hash_string(s):
    current = 0
    for c in s:
        current = ((current + ord(c)) * 17) % 256
    return current


def solve_pt1(data):
    return sum(hash_string(x) for x in data.split(','))


"""part2"""
def solve_part2_simple(data):
    boxes = {i: {} for i in range(256)}  # 用字典存储盒子
    
    for step in data.split(','):
        if '=' in step:
            label, focal = step.split('=')
            box_num = hash_string(label)
            boxes[box_num][label] = int(focal)
        else:
            label = step[:-1]  # 去掉最后的'-'
            box_num = hash_string(label)
            boxes[box_num].pop(label, None)  # 如果存在则删除
    
    # 计算能量
    total = 0
    for box_num, lenses in boxes.items():
        for slot, (_, focal) in enumerate(lenses.items(), 1):
            total += (box_num + 1) * slot * focal
            
    return total


if __name__ == "__main__":
    data = get_data(year=2023,day=15)
    print(f'part1: {solve_pt1(data)}')
    print(f'part2: {solve_part2_simple(data)}')
    
