from aocd import get_data
import re

def is_adjacent_to_symbol(schematic, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(schematic) and 0 <= c < len(schematic[0]) and schematic[r][c] not in '0123456789.':
            return True
    return False


def sum_part_numbers(schematic):
    total_sum = 0
    for idx, row in enumerate(schematic):
        for number in list(re.finditer(r'\d+', row)):
            if is_adjacent_to_symbol(schematic, idx, number.start()):
                total_sum += int(number.group())
    return total_sum


if __name__ == "__main__":
    data = get_data(year=2023,day=3)
    schematic = data.splitlines()
    print(sum_part_numbers(schematic)) 

