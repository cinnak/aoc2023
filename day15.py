from aocd import get_data

def hash_string(string):
    current = 0
    for c in string:
        current += ((ord(c)+current)*17)%256
    return current

def hash_string(s):
    current = 0
    for c in s:
        current = ((current + ord(c)) * 17) % 256
    return current

# Test it
print(hash_string('HASH'))  # Should print 52

def solve_pt1(data):
    return sum(hash_string(x) for x in data.split(','))




if __name__ == "__main__":
    data = get_data(year=2023,day=15)
    print(f'part1: {solve_pt1(data)}')
    # print(f'part2: {solve_pt2(data)}')
    
