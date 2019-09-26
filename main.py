import numpy as np
import random
import pandas as pd

values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
suits = ['_h', '_c', '_s', '_d']

# print(values)
# print(suits)

cards = []
for suit in suits:
    for value in values:
        card = value+suit
        cards.append(card)

# print(cards)
decks = []

#
# random_range = np.arange(0,1,.01)
# print(random_range)

# for _ in np.arange(0, 1, .01):
#     random.shuffle(cards, random=_)
#     decks.append(cards)
#     # print(decks)
# #
# #
# df = pd.DataFrame(decks)
# print(df.head())

# print(help(random))


# print(deck)
# print(help(random))

seeds = [x for x in np.arange(0,1,.01)]

for seed in seeds:

    # newcards = cards

    decks.append(cards)
    random.shuffle(cards)

df = pd.DataFrame(decks)
print(df.head())

# for x in seeds:
#     print(x)
