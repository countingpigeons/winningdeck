import numpy as np
import pandas as pd


def create_random_deck_indexes(n=5):
    np.random.seed(0)
    index = np.arange(0, 52)
    indexes = []
    for _ in np.arange(n):
        indexes.append(np.random.permutation(index))
    return indexes


class Base:
    suits = ['S', 'C', 'H', 'D']
    cards = list(np.arange(2, 11).astype('str'))
    cards.extend('JQKA')

    cardlables = []
    for suit in suits:
        for card in cards:
            cardlables.append(card+'_'+suit)


    cardvalues = cards * 4
    colors = ['Black']*26
    colors.extend(['Red']*26)

    tuples = list(zip(cardlables, cardvalues, colors))
    deck_df = pd.DataFrame(tuples)

    deck = pd.Series(cardlables)



class Deck:
    def __init__(self, index):
        self.deck = Base.deck[index].values
        self.deck_df = Base.deck_df.loc[index, :]
        self.cardvalues = Base.cardvalues
        self.colors = Base.colors
        self.tuples = Base.tuples
        self.index = index
        pass

    def summary(self):
        print('OriginalDeckOrder: {}'.format(self.deck))
        # print('CardValues: {}'.format(self.cardvalues))
        # print('Colors: {}'.format(self.colors))
        # print('Tuples: {}'.format(self.tuples))
        print('DeckDF: {}'.format(self.deck_df))
        print('Index: {}'.format(self.index))

    def deal_piles(self):
        pass

    def move_suits_up(self):
        pass

    def move_suits_down(self):
        pass

    def move_cards_between_piles(self):
        pass

    def deal_to_play_pile(self):
        pass

    def play_onto_piles(self):
        pass

#     HOW TO STORE CARD COLORS? IN A DICTIONARY AGAINST THE UNSORTED BASE.DECK PHAPS?
#     ALSO, I WILL WANT SOME KIND OF LOGGING AS WE 'PLAY' SO I CAN QA/SPOT-CHECK THE LOGIC (PHAPS W/ REAL DECK?)

def play(deck):
    # deck[]
    pass

def main():
    indexes = create_random_deck_indexes()
    deck = Deck(indexes[0])

    deck.summary()
    # print(deck.deck)
    # print(Base.deck.values)
    # print('ran main()')


main()
