import numpy as np
import random
import pandas as pd

values = ['2','3','4','5','6','7','8','9','10','j','q','k','a']
suits = ['_h','_c','_s','_d']

print(values)
print(suits)

cards = []
for suit in suits:
    for value in values:
        card = value+suit
        cards.append(card)

# print(cards)
decks = []
random.shuffle(cards)

decks.append(cards)
# print(decks)

df = pd.DataFrame(decks)

df.head()




# print(deck)

# print(help(random))