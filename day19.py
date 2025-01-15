from aocd import get_data
from math import prod

def parse_workflow(wf):
    name, rules = wf.split('{')
    rules = rules.strip('}').split(',')
    parsed_rules = []
    for r in rules[:-1]:
        cond, dest = r.split(':')
        var, op, val = cond[0], cond[1], int(cond[2:])
        parsed_rules.append((var, op, val, dest))
    parsed_rules.append(('', '', 0, rules[-1]))
    return {name: parsed_rules}

def parse_part(p):
    return {k:int(v) for k,v in [x.split('=') for x in p.strip('{}').split(',')]}

def process_part(workflows, part):
    curr = 'in'
    while curr not in 'AR':
        for var, op, val, dest in workflows[curr]:
            if not var or (op == '<' and part[var] < val) or (op == '>' and part[var] > val):
                curr = dest
                break
    return curr == 'A'

def solve_pt1():
    workflows, parts = inp.split('\n\n')
    workflows = {k:v for w in workflows.split('\n') for k,v in parse_workflow(w).items()}
    return sum(sum(p.values()) for p in map(parse_part, parts.split('\n')) if process_part(workflows, p))

"""part 2"""


class Range:
    def __init__(self, min=1, max=4000):
        self.min = min
        self.max = max
    
    def size(self):
        return max(0, self.max - self.min + 1)
    
    def split(self, op, val):
        if op == '<':
            return (Range(self.min, min(val-1, self.max)), 
                   Range(max(val, self.min), self.max))
        else:  # '>'
            return (Range(max(val+1, self.min), self.max), 
                   Range(self.min, min(val, self.max)))
    
    def copy(self):
        return Range(self.min, self.max)

def parse_workflows(workflows_str):
    workflows = {}
    for line in workflows_str.split('\n'):
        name, rules = line.split('{')
        rules = rules.strip('}').split(',')
        parsed_rules = []
        for r in rules[:-1]:
            cond, dest = r.split(':')
            var, op, val = cond[0], cond[1], int(cond[2:])
            parsed_rules.append((var, op, val, dest))
        parsed_rules.append(('', '', 0, rules[-1]))
        workflows[name] = parsed_rules
    return workflows

def count_accepted(workflows, ranges, curr='in'):
    if curr == 'R': 
        return 0
    if curr == 'A': 
        return prod(r.size() for r in ranges.values())
    
    total = 0
    for var, op, val, dest in workflows[curr]:
        if not var:
            total += count_accepted(workflows, ranges, dest)
            break
            
        curr_ranges = {k: v.copy() for k,v in ranges.items()}
        match, nomatch = curr_ranges[var].split(op, val)
        
        if match.size() > 0:
            curr_ranges[var] = match
            total += count_accepted(workflows, curr_ranges, dest)
            
        if nomatch.size() > 0:
            ranges[var] = nomatch
        else:
            break
            
    return total

def solve_pt2():
    workflows, _ = inp.split('\n\n')
    workflows = parse_workflows(workflows)
    ranges = {var: Range() for var in 'xmas'}
    return count_accepted(workflows, ranges)


if __name__ == "__main__":
    inp = get_data(year=2023, day=19)
    print(f'part 1: {solve_pt1()}')
    print(f'part 2: {solve_pt2()}')