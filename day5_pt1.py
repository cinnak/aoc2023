from typing import List, Dict, Tuple
from aocd import get_data

# 定义转换链作为全局常量
CONVERSION_CHAIN = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location'
]

def deal_raw_data(data: str) -> Tuple[List[int], Dict[str, List[Tuple[int, int, int]]]]:
    """
    处理原始输入数据，提取种子数字和映射规则。

    Args:
        data (str): 原始输入字符串

    Returns:
        Tuple[List[int], Dict[str, List[Tuple[int, int, int]]]]: 
            - 种子数字列表
            - 映射规则字典，其中键为映射名称，值为包含(目标起始，源起始，长度)的元组列表

    Raises:
        ValueError: 当输入数据格式不正确时抛出
    """
    sections = data.split('\n\n')
    if len(sections) < 8:
        raise ValueError("数据格式不正确：缺少必要的数据段")
    try:
        seeds = list(map(int, sections[0].split(': ')[1].split()))
    except (IndexError, ValueError) as e:
        raise ValueError("种子数据格式不正确") from e
    
    mappings = {}
    for section in sections[1:]:
        try:
            name = section.split(':\n')[0].split(' ')[0]
            numbers = section.split(':\n')[1].split('\n')
            mapping_rules = []
            for x in numbers:
                if x.strip():
                    nums = tuple(map(int, x.split()))
                    if len(nums) == 3:
                        mapping_rules.append(nums)
            mappings[name] = mapping_rules
        except (IndexError, ValueError) as e:
            raise ValueError(f"映射数据 {name} 格式不正确") from e
    return seeds, mappings

def map_number(seed: int, mapping: List[Tuple[int, int, int]]) -> int:
    """
    将单个数字通过给定的映射规则转换为新的数字。

    Args:
        seed (int): 输入数字
        mapping (List[Tuple[int, int, int]]): 映射规则列表

    Returns:
        int: 转换后的数字
    """
    for dest_start, src_start, length in mapping:
        if src_start <= seed < src_start + length:
            return dest_start + (seed - src_start)
    return seed

def seed_to_location(seed: int, mappings: Dict[str, List[Tuple[int, int, int]]]) -> int:
    """
    将种子号码通过一系列映射转换为最终位置。

    Args:
        seed (int): 种子号码
        mappings (Dict[str, List[Tuple[int, int, int]]]): 所有映射规则

    Returns:
        int: 最终位置号码
    """
    current = seed
    for convert in CONVERSION_CHAIN:
        current = map_number(current, mappings[convert])
    return current
if __name__ == "__main__":
    data = get_data(year=2023, day=5)
    seeds, mappings = deal_raw_data(data)
    min_location = min(seed_to_location(x, mappings) for x in seeds)
    print(f'pt1: {min_location}')

