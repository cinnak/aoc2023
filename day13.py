from aocd import get_data
import numpy as np
def data_process():
    data = get_data(year=2023, day=13)
    patterns = [p.split('\n') for p in data.strip().split('\n\n')]
    return patterns

def check_horizontal_mirror(pattern):
    for i in range(1, len(pattern)):
        if pattern[i-1] == pattern[i]:  # 找到相邻相同的行
            is_mirror = all(pattern[i-1-j] == pattern[i+j] for j in range(1, min(i, len(pattern) - i)))
            if is_mirror:
                return i
    return 0

def get_vertical_mirror(pattern):
    # 转置图案
    transposed = [''.join(col) for col in zip(*pattern)]
    return check_horizontal_mirror(transposed)

def score_pt1(patterns):
    total = 0
    for pattern in patterns:
        h = check_horizontal_mirror(pattern)
        v = get_vertical_mirror(pattern)
        score = h * 100 + v
        total += score
    return total  



def mirrorpos(arr, axis=0, diff=1):
    m = np.array(arr, dtype=int)
    if axis == 1:
        m = m.T
    for i in range(m.shape[0] - 1):
        upper_flipped = np.flip(m[: i + 1], axis=0)
        lower = m[i + 1 :]
        rows = min(upper_flipped.shape[0], lower.shape[0])
        if np.count_nonzero(upper_flipped[:rows] - lower[:rows]) == diff:
            return i + 1
    return 0

def solve_pt2():
    data = get_data(year=2023,day=13).split('\n\n')
    i=1
    total = 0
    for puzzle in data:
        arr = []
        for line in puzzle.splitlines():
            arr.append([*line.strip().replace(".", "0").replace("#", "1")])
        total += 100 * mirrorpos(arr, axis=0, diff=i) + mirrorpos(arr, axis=1, diff=i)
    return total 


if __name__ == "__main__":
    patterns = data_process()
    # print(f"Part 1: {score_pt1(patterns)}")
    print(f'part 2: {solve_pt2()}')
    

    
    
    