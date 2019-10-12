import random

def create_random_deck_indexes(n=5):
    index = [i for i in range(0, 52)]
    indicies = []
    j = 0
    while j < n:
        random.seed(j)
        randindex = index.copy()
        random.shuffle(randindex)
        indicies.append(randindex)
        j += 1

    # print(indicies)
    return indicies

class Base:
    suits = ['S', 'C', 'H', 'D']
    suits52 = []
    for suit in suits:
        suits52.extend(suit * 13)

    cardvals = [str(card) for card in range(2, 11)] + ['J', 'Q', 'K', 'A']
    labels52 = []
    for suit in suits:
        for card in cardvals:
            labels52.append(card + '_' + suit)

    # now that cardvals has been used for labels, reset this with pure numeric values to make play easier.
    cardvals = [card for card in range(2, 14)] + [1]
    cardvals52 = cardvals * 4
    colors52 = ['Black'] * 26 + ['Red'] * 26

    rawdeck = [list(item) for item in zip(labels52, cardvals52, colors52, suits52)]


class SolitaireGame:
    label = 0
    val = 1
    color = 2
    suit = 3

    def __init__(self, randindex):
        # add this specific randindex to rawdeck and sort it by this index.
        deck = []
        i = 0
        for item in Base.rawdeck:
            deck.append(item + [randindex[i]])
            i += 1
        deck = sorted(deck, key=lambda x: x[4])
        # deck = [tuple(item) for item in deck]
        deck = list(map(lambda x: {'label': x[0], 'value': x[1], 'color': x[2], 'suit': x[3]}, deck))
        self.deck = deck

    def summary(self):
        # print('OriginalDeckOrder: {}\n'.format(Base.rawdeck))
        print('ShuffledDeck: {}\n'.format(list(map(lambda x: x['label'], self.deck))))
        # print(color)
        pass

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

#     ALSO, I WILL WANT SOME KIND OF LOGGING AS WE 'PLAY' SO I CAN QA/SPOT-CHECK THE LOGIC (PHAPS W/ REAL DECK?)


def PlaySolitaire(numdecks):

    decks = create_random_deck_indexes(numdecks)
    game = SolitaireGame(decks[0])

    # print(game.deck[:3][-1])
    # print('')
    game.summary()
    print('_____ran PlaySolitaire()_____')


if __name__ == "__main__":
    PlaySolitaire(numdecks=8)
