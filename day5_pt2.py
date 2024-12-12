from typing import List, Tuple, Optional
from dataclasses import dataclass
from aocd import get_data

@dataclass
class Range:
    """表示一个范围的数据类"""
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length

    def intersect(self, other: 'Range')->Optional['Range']:
        """检查两个范围是否相交"""
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start < end:
            return Range(start, end - start)
        return None

@dataclass
class Mapping:
    """表示一个映射规则"""
    source_start: int
    dest_start: int
    length: int

    def get_source_range(self)->Range:
        return Range(self.source_start, self.length)

    def map_range(self, input_range:Range)-> tuple[Optional[Range], list[Range]]:
        """映射一个输入范围，返回映射后的范围和未映射的范围列表"""
        source_range = self.get_source_range()
        intersection = input_range.intersect(source_range)
        if not intersection:
            return None, [input_range]
        # 计算映射后的范围和未映射的范围
        offset = intersection.start - source_range.start
        mapped_range = Range(self.dest_start + offset, intersection.length)
        # 处理未映射的部分
        unmapped_range = []
        if input_range.start < intersection.start:
            unmapped_range.append(Range(source_range.start, intersection.start - source_range.start))
        if intersection.end < input_range.end:
            unmapped_range.append(Range(intersection.end, input_range.end - intersection.end))
        return mapped_range, unmapped_range

@dataclass
class MapChain:
    """处理整个映射链"""
    seed_ranges: list[Range]
    mappings: list[list[Mapping]]

    @classmethod
    def from_raw_data(cls, data: str)->'MapChain':
        """从原始数据创建MapChain实例"""
        sections = data.split('\n\n')
        if len(sections) < 8:
            raise ValueError("数据格式不正确：缺少必要的数据段")
        # 处理种子范围
        seed_numbers = list(map(int, sections[0].split(': ')[1].split()))
        seed_ranges = []
        for i in range(0,len(seed_numbers),2):  
            start = seed_numbers[i]
            length = seed_numbers[i+1]
            seed_ranges.append(Range(start, length))

        # 处理每个映射
        all_mappings = []
        for section in sections[1:]:
            rules = section.split('\n')[1:]
            section_mappings = []
            for rule in rules:
                if rule.strip():
                    dest_start, source_start, length = map(int, rule.split())
                    section_mappings.append(Mapping(source_start, dest_start, length))
            all_mappings.append(section_mappings)
        return cls(seed_ranges, all_mappings)
    
    def map_range_through_rules(self, input_range: Range, mappings: list[Mapping]) -> list[Range]:
        """将一个范围通过一组映射规则转换"""
        result = []
        unmapped = [input_range]
        
        for mapping in mappings:
            new_unmapped = []
            for range_to_map in unmapped:
                mapped, remaining = mapping.map_range(range_to_map)
                if mapped:
                    result.append(mapped)
                new_unmapped.extend(remaining)
            unmapped = new_unmapped
        
        result.extend(unmapped)
        return result

    def apply_single_mapping_layer(self, ranges: list[Range], layer_mappings: list[Mapping]) -> list[Range]:
        """应用单层映射规则到输入范围列表"""
        result_ranges = []
        for input_range in ranges:
            result_ranges.extend(self.map_range_through_rules(input_range, layer_mappings))
        return result_ranges

    def process_range(self, input_range: Range) -> list[Range]:
        """处理一个范围通过整个映射链的转换"""
        current_ranges = [input_range]
        for layer_mappings in self.mappings:
            current_ranges = self.apply_single_mapping_layer(current_ranges, 
                                                          layer_mappings)
        return current_ranges

    def find_min_location(self) -> int:
        """找出所有种子范围对应的最小位置值"""
        min_location = float('inf')
        total_ranges = len(self.seed_ranges)
        
        for i, seed_range in enumerate(self.seed_ranges, 1):
            print(f"处理种子范围 {i}/{total_ranges}: {seed_range}")
            location_ranges = self.process_range(seed_range)
            for range in location_ranges:
                min_location = min(min_location, range.start)
                
        return int(min_location)

def solve_part2(data: str) -> int:
    """解决第二部分的问题"""
    chain = MapChain.from_raw_data(data)
    return chain.find_min_location()
    
        
if __name__ == "__main__":
    data = get_data(year=2023, day=5)
    print(solve_part2(data))