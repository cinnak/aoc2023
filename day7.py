from aocd import get_data
import math
import re
from collections import Counter

def card_type(card):
    if len(card) != 5:
        return 'not a valid card'
    values = sorted(list(Counter(card).values()))
    
    match values:
        case [5]:          return 7  # Five of a kind
        case [1, 4]:       return 6  # Four of a kind
        case [2, 3]:       return 5  # Full house
        case [1, 1, 3]:    return 4  # Three of a kind
        case [1, 2, 2]:    return 3  # Two pair
        case [1, 1, 1, 2]: return 2  # One pair
        case _:            return 1  # High card

def card_mapping(cards):
    card_values = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
    }
    result = {}
    for card in cards:
        t = ''.join(str(card_values[o]).zfill(2) for o in card)
        result[card] = t
    return result

def get_sort_key(card):
    # 返回一个元组 (牌型, 牌面值)
    card_str = card.split()[0]  # 因为输入格式是 "AK998 123"，需要分离牌和bid
    return (card_type(card_str), card_mapping([card_str])[card_str])

"""part 2"""
def card_type_pt2(card):
    if len(card) != 5:
        return 'not a valid card'    
    # 如果全是J，直接返回最高牌型
    if card == 'JJJJJ':
        return 7  
    # 统计非J牌中出现最多的牌
    count_without_j = Counter(c for c in card if c != 'J')
    if not count_without_j:  # 如果没有非J的牌
        return 7
    most_common = count_without_j.most_common(1)[0][0]
    
    # 把J都变成出现最多的牌
    new_card = card.replace('J', most_common)
    after = Counter(new_card)
    values = sorted(list(after.values()))
    
    match values:
        case [5]:          return 7  # Five of a kind
        case [1, 4]:       return 6  # Four of a kind
        case [2, 3]:       return 5  # Full house
        case [1, 1, 3]:    return 4  # Three of a kind
        case [1, 2, 2]:    return 3  # Two pair
        case [1, 1, 1, 2]: return 2  # One pair
        case _:            return 1  # High card

def card_mapping_pt2(cards):
    card_values = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 1, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
    }
    result = {}
    for card in cards:
        t = ''.join(str(card_values[o]).zfill(2) for o in card)
        result[card] = t
    return result

def get_sort_key_pt2(card):
    # 返回一个元组 (牌型, 牌面值)
    card_str = card.split()[0]  # 因为输入格式是 "AK998 123"，需要分离牌和bid
    return (card_type_pt2(card_str), card_mapping_pt2([card_str])[card_str])






if __name__ == "__main__":
    data = get_data(year=2023, day=7).splitlines()
    # part 1
    sorted_data_pt1 = sorted(data, key=get_sort_key)
    total_pt1 = sum([(idx+1) * int(card.split()[1]) for idx,card in enumerate(sorted_data_pt1)])
    print(f'pt1: {total_pt1}')

    # part 2
    sorted_data_pt2 = sorted(data, key=get_sort_key_pt2)
    total_pt2 = sum([(idx + 1) * int(card.split()[1]) for idx,card in enumerate(sorted_data_pt2)])
    print(f'pt2: {total_pt2}')


