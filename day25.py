import networkx as nx

from aocd import get_data
from typing import List, Set, Tuple

def parse_line(line: str) -> Tuple[str, List[str]]:
    """解析输入的每一行"""
    node, connections = line.split(": ")
    return node, connections.split()

def build_graph(data: List[str]) -> nx.Graph:
    """构建无向图"""
    G = nx.Graph()
    for line in data:
        node, connected_nodes = parse_line(line)
        G.add_edges_from((node, n) for n in connected_nodes)
    return G

def find_cut_components(G: nx.Graph) -> Tuple[Set, List[Set]]:
    """找到最小割和分割后的组件"""
    min_cut = nx.minimum_edge_cut(G)
    G2 = G.copy()
    G2.remove_edges_from(min_cut)
    return min_cut, list(nx.connected_components(G2))

def calculate_result(components: List[Set]) -> int:
    """计算结果"""
    sizes = [len(component) for component in components]
    return sizes[0] * sizes[1]


def solve_day25():
    """主函数"""
    # 获取数据
    data = get_data(year=2023, day=25).splitlines()
    
    # 处理数据
    G = build_graph(data)
    min_cut, components = find_cut_components(G)
    result = calculate_result(components)
    
    # 输出结果
    print("答案(两组大小的乘积):", result)
    
   
    
    return result





if __name__ == "__main__":
    solve_day25()
