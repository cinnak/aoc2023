from aocd import get_data



def pt1(data):
    result = 0
    for x in data:
        winning_numbers, holding_numbers = x.split(": ")[1].split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        holding_numbers = set(map(int, holding_numbers.split()))

        # Calculate the number of matches
        c = len(winning_numbers & holding_numbers)

        # Calculate points based on matches
        result += 0 if c == 0 else 2 ** (c - 1)
        
    return result

def pt2(data):
    # for each card, calculate matches
    match_cards = []
    for x in data:
        winning_numbers, holding_numbers = x.split(": ")[1].split("|")
        winning_numbers = set(map(int, winning_numbers.split()))
        holding_numbers =  set(map(int, holding_numbers.split()))

        # Calculate the number of matches
        c = len(winning_numbers & holding_numbers)
        match_cards.append(c)
    
    # initiate card instaces
    card_instances = [1]*len(match_cards)
    # make copies of each card according to matches
    for i, matches in enumerate(match_cards):
        for j in range(i + 1, min(i + matches + 1, len(match_cards))):
            card_instances[j] += card_instances[i]
            
    return sum(card_instances)

    

if __name__=="__main__":
    data = get_data(year=2023,day=4)
    data = data.splitlines()
    result_pt1 = pt1(data)
    print(f'pt1: {result_pt1}')
    result_pt2= pt2(data)
    print(f'pt2: {result_pt2}')
