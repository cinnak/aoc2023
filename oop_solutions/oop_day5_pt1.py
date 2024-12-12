from aocd import get_data
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Almanac:
    seeds:List
    mappings:Dict[str,List[Tuple[int,int,int]]]

    # 定义转换链作为类属性
    CONVERSION_CHAIN = [
        'seed-to-soil',
        'soil-to-fertilizer',
        'fertilizer-to-water',
        'water-to-light',
        'light-to-temperature',
        'temperature-to-humidity',
        'humidity-to-location'
    ]

    @classmethod
    def from_raw_data(cls,data:str)->'Almanac':
        """从原始数据创建Almanac实例"""
        seeds, mappings = cls._parse_raw_data(data)
        return cls(seeds=seeds, mappings=mappings)

    @staticmethod
    def _parse_raw_data(data: str) -> Tuple[List[int], Dict]:
        # 纯功能性的方法，不依赖于类的状态
        # 分割数据块
        sections = data.split('\n\n')
        if len(sections) < 8:
            raise ValueError("数据格式不正确：缺少必要的数据段")
        
        # 处理种子数据
        try:
            seeds = list(map(int, sections[0].split(': ')[1].split()))
        except (IndexError, ValueError) as e:
            raise ValueError("种子数据格式不正确") from e
        
        # 处理映射数据
        mappings = {}
        for section in sections[1:]:
            try:
                name = section.split(':\n')[0].split(' ')[0]
                numbers = section.split(':\n')[1].split('\n')
                map_num = []
                for x in numbers:
                    if x.strip():
                        nums = tuple(map(int, x.split()))
                        if len(nums) == 3:
                            map_num.append(nums)
                mappings[name] = map_num
            except (IndexError, ValueError) as e:
                raise ValueError(f"映射数据 {name} 格式不正确") from e
        
        return seeds, mappings

    def map_number(self, number: int, mapping: List[Tuple[int, int, int]]) -> int:
        """单个数字的映射转换"""
        for dest_start, src_start, length in mapping:
            if src_start <= number < src_start + length:
                return dest_start + (number - src_start)
        return number

    def get_location(self, seed: int) -> int:
        """获取单个种子对应的位置"""
        current = seed
        for step in self.CONVERSION_CHAIN:
            current = self.map_number(current, self.mappings[step])
            # logger.debug(f"{step}: {current}")
        return current

    def find_min_location(self) -> int:
        """找出所有种子对应的最小位置"""
        # logger.info(f"Processing {len(self.seeds)} seeds...")
        return min(self.get_location(seed) for seed in self.seeds)

def main():
    """主函数"""
    from aocd import get_data
    
    # 获取数据并创建Almanac实例
    data = get_data(year=2023, day=5)
    almanac = Almanac.from_raw_data(data)
    
    # 计算结果
    result = almanac.find_min_location()
    print(f"最小位置值: {result}")

if __name__ == "__main__":
    main()
