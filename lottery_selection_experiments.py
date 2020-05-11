import random
# this is a series of experiments to determine the effectiveness of
# biased random selection.
ten_percent = 1
seventy_percent = 7
twenty_percent = 2

# Make a list, then append 0,1,or 2 for each point of the values given.
# pick a random integer between 0 and length of the list.
# use random integer to pull number stored at that position
# that is the winner.
# Simple, but limited to integers

def lotto():
    participants = [ten_percent,seventy_percent,twenty_percent]
    lottery_bag = []
    for x in participants:
        for y in range(0,x):
            lottery_bag.append(x)
    winning_spot = random.randint(0, (len(lottery_bag)-1))
    winner = lottery_bag[winning_spot]
    return winner


def result_interpreter(argument):
    switcher = {
        1: "ten",
        7: "seventy",
        2: "twenty",
    }
    return switcher.get(argument, "nothing")

def lotto_test():
    results = {"ten": 0, "seventy": 0, "twenty": 0}
    random.seed()
    max_range = 4
    for x in range(0,10**max_range):
        numeric_winner = lotto()
        winrar = result_interpreter(numeric_winner)
        results[winrar] = results[winrar]+1
    for x in results:
        as_percent = results[x]/10**(max_range - 2)
        print(x," percent occured: ", as_percent, "% of the time")

lotto_test()

# each claims a specific area and then a random float is chosen
# between 0 and the highest value. area size is based on previous
# maximum and the value given (pheromone)


def range_based():
    participants = [ten_percent, seventy_percent, twenty_percent]
    random.seed()
    range_start = 0
    ranges = []
    sum = 0
    for x in participants:
        sum += x

    for x in participants:
        ranges.append([range_start, range_start+x])
        range_start = range_start + x
    print(ranges)
    random_float = random.uniform(0,sum)
    print(random_float)
    current = 0
    winner = None
    for range in ranges:
        if random_float >= range[0] and random_float < range[1]:
            print("float value in range of")
            print(range)
            winner = participants[current]
        else:
            current += 1

    return winner


range_based()
def range_test():
    results = {"ten": 0, "seventy": 0, "twenty": 0}
    random.seed()
    max_range = 4
    for x in range(0,10**max_range):
        numeric_winner = range_based()
        winrar = result_interpreter(numeric_winner)
        results[winrar] = results[winrar]+1