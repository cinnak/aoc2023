from aocd import get_data
from itertools import combinations

def find_swell(data):
    rows_to_swell = []
    for idx, row in enumerate(data):
        if all(x=='.' for x in row):
            rows_to_swell.append(idx)

    cols_to_swell = []
    for j in range(len(data[0])):
        if all(data[i][j]=='.' for i in range(len(data))):
            cols_to_swell.append(j)
    return rows_to_swell, cols_to_swell

def find_galaxy_pairs(data):
    galaxies = []
    for i, row in enumerate(data):
        for j in range(0,len(data[0])):
            if data[i][j] == '#':
                galaxies.append((i,j))
    pairs = list(combinations(galaxies, 2))
    return pairs

def count_empty_spaces(g1, g2, rows_to_swell, cols_to_swell):
    # 获取行范围
    x1, x2 = g1[0], g2[0]
    row_range = range(min(x1, x2), max(x1, x2) + 1)
    
    # 获取列范围
    y1, y2 = g1[1], g2[1]
    col_range = range(min(y1, y2), max(y1, y2) + 1)
    
    # 计算经过的空行和空列数量
    empty_rows = sum(1 for x in row_range if x in rows_to_swell)
    empty_cols = sum(1 for y in col_range if y in cols_to_swell)
    
    return empty_rows, empty_cols

def calculate_distance(g1, g2, rows_to_swell, cols_to_swell):
    # 基础曼哈顿距离
    manhattan_dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    
    # 计算空行空列
    empty_r, empty_c = count_empty_spaces(g1, g2, rows_to_swell, cols_to_swell)
    
    # 每个空行空列都要多走一步
    return manhattan_dist + empty_r + empty_c

def part1(data):
    rows_to_swell, cols_to_swell = find_swell(data)
    pairs = find_galaxy_pairs(data)
    total_distance = sum(
        calculate_distance(g1, g2, rows_to_swell, cols_to_swell) 
        for g1, g2 in pairs
    )
    return total_distance

"""part2"""
def calculate_distance_pt2(g1, g2, rows_to_swell, cols_to_swell):
    # 基础曼哈顿距离
    manhattan_dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    
    # 计算空行空列
    empty_r, empty_c = count_empty_spaces(g1, g2, rows_to_swell, cols_to_swell)
    
    # 每个空行空列都要多走一步
    return manhattan_dist + empty_r*999999 + empty_c*999999


def part2(data):
    rows_to_swell, cols_to_swell = find_swell(data)
    pairs = find_galaxy_pairs(data)
    total_distance = sum(
        calculate_distance_pt2(g1, g2, rows_to_swell, cols_to_swell) 
        for g1, g2 in pairs
    )
    return total_distance

if __name__ == "__main__":
    data = get_data(year=2023,day=11).splitlines()
    total_distance = part1(data)
    print(f"part1 总距离和: {total_distance}")
    total_distance = part2(data)
    print(f"part2 总距离和: {total_distance}")

