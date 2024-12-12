from aocd import get_data
import math
import re

def deal_raw_data(data):
    times, records = data.splitlines()
    times = [int(x) for x in re.findall(r'\d+',times)]
    records = [int(x) for x in re.findall(r'\d+',records)]
    games = list(zip(times,records))
    return games

def valid_rounds(games):
    # brute force is inefficient
    result = []
    for game in games:
        press = 0
        valid_rounds = 0
        while press <= game[0]:
            move = game[0] - press
            distance = press*move
            if distance>=game[1]:
                valid_rounds += 1       
            press += 1
        result.append(valid_rounds)
    return math.prod(result)

def quadratic_solutions(T,D):
    # 解 -x² + Tx - D = 0
    # 使用求根公式：x = (-b ± √(b² - 4ac)) / (2a)
    a = -1
    b = T
    c = -D
    
    discriminant = b*b - 4*a*c
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    return x1, x2
    
def count_winning_ways(T, D):
    x1, x2 = quadratic_solutions(T, D)
    # 向上取整x1，向下取整x2
    start = math.ceil(x1)
    end = math.floor(x2)
    return end - start + 1




def valid_rounds2(data):
    times, distance = data.splitlines()
    times = int(''.join(x for x in re.findall(r'\d+',times)))
    distance = int(''.join(x for x in re.findall(r'\d+',distance)))
    result=count_winning_ways(times,distance)
    return result



if __name__ == "__main__":
    data = get_data(year=2023, day=6)
    # part 1
    # games = deal_raw_data(data)
    # print()'part1':,valid_rounds(games))

    # part 2
    print('part2:',valid_rounds2(data))
