from aocd import get_data
from collections import deque
from enum import Enum
from math import lcm


class Pulse(Enum):
    LOW = 0
    HIGH = 1

class Module:
    def __init__(self, name, type_, targets):
        self.name = name
        self.type = type_
        self.targets = targets
        self.state = False  # for flip-flops
        self.memory = {}    # for conjunctions

def parse_input(data):
    modules = {}
    for line in data:
        source, targets = line.split(' -> ')
        targets = targets.split(', ')
        if source == 'broadcaster':
            modules[source] = Module(source, 'B', targets)
        else:
            modules[source[1:]] = Module(source[1:], source[0], targets)
    return modules

def init_modules(modules):
    # 初始化连接器的记忆
    for source in modules.values():
        for target_name in source.targets:
            if target_name in modules and modules[target_name].type == '&':
                modules[target_name].memory[source.name] = Pulse.LOW

def process_signals(modules):
    signals = deque([('button', Pulse.LOW, 'broadcaster')])
    counts = {Pulse.LOW: 1, Pulse.HIGH: 0}
    
    while signals:
        source, pulse, target = signals.popleft()
        if target not in modules:
            continue
            
        module = modules[target]
        next_pulse = None
        
        if module.type == 'B':
            next_pulse = pulse
        elif module.type == '%' and pulse == Pulse.LOW:
            module.state = not module.state
            next_pulse = Pulse.HIGH if module.state else Pulse.LOW
        elif module.type == '&':
            module.memory[source] = pulse
            next_pulse = Pulse.LOW if all(p == Pulse.HIGH for p in module.memory.values()) else Pulse.HIGH
            
        if next_pulse is not None:
            for next_target in module.targets:
                signals.append((target, next_pulse, next_target))
                counts[next_pulse] += 1
                
    return counts[Pulse.LOW], counts[Pulse.HIGH]

def solve_pt1():
    data = get_data(year=2023, day=20).splitlines()
    modules = parse_input(data)
    init_modules(modules)
    
    total_low = total_high = 0
    for _ in range(1000):
        low, high = process_signals(modules)
        total_low += low
        total_high += high
        
    return total_low * total_high

"""part 2"""


class Pulse(Enum):
    LOW = 0
    HIGH = 1

class Module:
    def __init__(self, name, type_, targets):
        self.name = name
        self.type = type_
        self.targets = targets
        self.state = False  # for flip-flops
        self.memory = {}    # for conjunctions

def parse_input(data):
    modules = {}
    for line in data:
        source, targets = line.split(' -> ')
        targets = targets.split(', ')
        if source == 'broadcaster':
            modules[source] = Module(source, 'B', targets)
        else:
            modules[source[1:]] = Module(source[1:], source[0], targets)
    return modules

def init_modules(modules):
    for source in modules.values():
        for target_name in source.targets:
            if target_name in modules and modules[target_name].type == '&':
                modules[target_name].memory[source.name] = Pulse.LOW

def find_rx_source(modules):
    for name, module in modules.items():
        if 'rx' in module.targets:
            return name
    return None

def monitor_inputs(modules, target_module):
    cycles = {}
    press_count = 0
    input_sources = list(modules[target_module].memory.keys())
    
    while len(cycles) < len(input_sources):
        press_count += 1
        signals = deque([('button', Pulse.LOW, 'broadcaster')])
        
        while signals:
            source, pulse, target = signals.popleft()
            
            if source in input_sources and pulse == Pulse.HIGH:
                if source not in cycles:
                    cycles[source] = press_count
            
            if target not in modules:
                continue
                
            module = modules[target]
            next_pulse = None
            
            if module.type == 'B':
                next_pulse = pulse
            elif module.type == '%' and pulse == Pulse.LOW:
                module.state = not module.state
                next_pulse = Pulse.HIGH if module.state else Pulse.LOW
            elif module.type == '&':
                module.memory[source] = pulse
                next_pulse = Pulse.LOW if all(p == Pulse.HIGH for p in module.memory.values()) else Pulse.HIGH
                
            if next_pulse is not None:
                for next_target in module.targets:
                    signals.append((target, next_pulse, next_target))
    
    return cycles

def solve_part2():
    data = get_data(year=2023, day=20).splitlines()
    modules = parse_input(data)
    init_modules(modules)
    
    # 找到rx的输入源（一个连接器模块）
    rx_source = find_rx_source(modules)
    
    # 找到每个输入的循环周期
    cycles = monitor_inputs(modules, rx_source)
    
    # 计算最小公倍数
    return lcm(*cycles.values())





if __name__ == "__main__":
    data = get_data(year=2023, day=20)
    print(f"Part 1 答案: {solve_pt1()}")
    print(f"Part 2 答案: {solve_part2()}")
