from aocd import get_data
from typing import Dict, Tuple
from math import lcm

def parse_input(data: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    instructions, network = data.split('\n\n')
    nodes = {
        node.split(' = ')[0]: tuple(node.split(' = ')[1].strip('()').split(', '))
        for node in network.splitlines()
    }
    return instructions, nodes

def count_steps_to_zzz(instructions: str, nodes: Dict[str, Tuple[str, str]]) -> int:
    current = 'AAA'
    steps = 0
    instruction_len = len(instructions)
    
    while current != 'ZZZ':
        idx = 0 if instructions[steps % instruction_len] == 'L' else 1
        current = nodes[current][idx]
        steps += 1
    return steps
def part1(data: str) -> int:
    return count_steps_to_zzz(*parse_input(data))

"""part 2"""
def find_cycle_length(start: str, instructions: str, nodes: Dict[str, Tuple[str, str]]) -> int:
    current = start
    steps = 0
    instruction_len = len(instructions)
    
    while not current.endswith('Z'):
        idx = 0 if instructions[steps % instruction_len] == 'L' else 1
        current = nodes[current][idx]
        steps += 1
    return steps



def part2(data: str) -> int:
    instructions, nodes = parse_input(data)
    # 找到所有以 'A' 结尾的起始节点
    start_nodes = [node for node in nodes.keys() if node.endswith('A')]
    
    # 计算每个起始节点到达Z结尾节点的周期
    cycles = [find_cycle_length(node, instructions, nodes) for node in start_nodes]
    
    # 返回所有周期的最小公倍数
    return lcm(*cycles)

if __name__ == "__main__":
    data = get_data(year=2023, day=8)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")