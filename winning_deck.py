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

    # now that cardvals has been used for labels, reset this with pure numeric
    # values to make play easier.
    cardvals = [card for card in range(2, 14)] + [1]
    cardvals52 = cardvals * 4
    colors52 = ['Black'] * 26 + ['Red'] * 26

    deck = [list(item) for item in
            zip(labels52, cardvals52, colors52, suits52)]


class SolitaireGame:

    def __init__(self, randindex):
        # add this specific randindex to rawdeck and sort it by this index.
        deck = []
        i = 0
        for item in Base.deck:
            deck.append(item + [randindex[i]])
            i += 1
        deck = sorted(deck, key=lambda x: x[4])
        # deck = [tuple(item) for item in deck] # tuple safer, but inconvenient
        deck = list(
            map(lambda x: {'label': x[0], 'value': x[1],
                           'color': x[2], 'suit': x[3]}, deck))
        self.deck = deck
        self.spade_pile = []
        self.club_pile = []
        self.heart_pile = []
        self.diamond_pile = []
        self.pile1 = []
        self.pile2 = []
        self.pile2_hidden = []
        self.pile3 = []
        self.pile3_hidden = []
        self.pile4 = []
        self.pile4_hidden = []
        self.pile5 = []
        self.pile5_hidden = []
        self.pile6 = []
        self.pile6_hidden = []
        self.pile7 = []
        self.pile7_hidden = []
        self.play_pile = []
        # self.reserve_pile = []

    def summary(self):

        piles = [self.pile1, self.pile2, self.pile3,
                 self.pile4, self.pile5,
                 self.pile6, self.pile7]

        for pile in piles:
            print((pile[0]['label']))

        # print('OriginalDeckOrder: {}\n'.format(Base.deck))
        # print('ShuffledDeck: {}\n'.format(list(map(lambda x: x['label'],
        #                                            self.deck))))
        # for card in self.deck:
        #     print(card['label'])

        print('_____ran summary_____')
        pass

    def deal_piles(self):

        if len(self.deck) == 52:
            hiddenpiles = [self.pile2_hidden, self.pile3_hidden,
                           self.pile4_hidden, self.pile5_hidden,
                           self.pile6_hidden, self.pile7_hidden]

            piles = [self.pile1, self.pile2, self.pile3,
                     self.pile4, self.pile5,
                     self.pile6, self.pile7]

            self.pile1.append(self.deck.pop(0))
            for pile in hiddenpiles[:]:
                pile.append(self.deck.pop(0))

            self.pile2.append(self.deck.pop(0))
            for pile in hiddenpiles[1:]:
                pile.append(self.deck.pop(0))

            self.pile3.append(self.deck.pop(0))
            for pile in hiddenpiles[2:]:
                pile.append(self.deck.pop(0))

            self.pile4.append(self.deck.pop(0))
            for pile in hiddenpiles[3:]:
                pile.append(self.deck.pop(0))

            self.pile5.append(self.deck.pop(0))
            for pile in hiddenpiles[4:]:
                pile.append(self.deck.pop(0))

            self.pile6.append(self.deck.pop(0))
            for pile in hiddenpiles[5:]:
                pile.append(self.deck.pop(0))

            self.pile7.append(self.deck.pop(0))

# test out
            # for pile in hiddenpiles:
            #     print((pile))
            # for pile in piles:
            #     print((pile))
            # for card in self.pile7_hidden:
            #     print(card['label'])
            # print(self.pile7_hidden)
            print('_____ran deal_piles_____')

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

#     ALSO, I WILL WANT SOME KIND OF LOGGING AS WE 'PLAY' SO I CAN
# QA/SPOT-CHECK THE LOGIC (PHAPS W/ REAL DECK?)


def main(numdecks):

    decks = create_random_deck_indexes(numdecks)
    game = SolitaireGame(decks[0])
    game.deal_piles()

    # print(game.deck[:3][-1])
    # print('')
    # print(game.deck)
    game.summary()
    print('_____ran main_____')


if __name__ == "__main__":
    main(numdecks=8)
