import random
import logging
logging.basicConfig(filename='winning_deck_moves.log', level=logging.DEBUG)


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

    spade_pile = []
    club_pile = []
    heart_pile = []
    diamond_pile = []
    pile1 = []
    pile1_hidden = []  # created to simplify indexing. will remain empty.
    pile2 = []
    pile2_hidden = []
    pile3 = []
    pile3_hidden = []
    pile4 = []
    pile4_hidden = []
    pile5 = []
    pile5_hidden = []
    pile6 = []
    pile6_hidden = []
    pile7 = []
    pile7_hidden = []
    suit_piles = [spade_pile, club_pile, heart_pile, diamond_pile]
    hidden_piles = [pile1_hidden, pile2_hidden, pile3_hidden, pile4_hidden,
                    pile5_hidden, pile6_hidden, pile7_hidden]
    piles = [pile1, pile2, pile3, pile4, pile5, pile6, pile7]
    play_pile = []
    game_lost = False
    game_won = False
    move_number = 0
    # moved = False

    def __init__(self, randindex):
        # add this specific randindex to base.deck and sort it by this index.
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

    def summary(self):
        pile_index = 0
        print('Piles:')
        for pile in self.piles:
            print('Pile {}:'.format(pile_index), end='')
            if len(pile) > 0:
                print([card['label'] for card in pile])
            else:
                print('na')
            pile_index += 1
        print('Play Pile: ', end='')
        if len(self.play_pile) > 0:
            print(self.play_pile[-1]['label'])
        else:
            print('N/A')
        # print('Deck:')
        # for card in self.deck:
        #     print(card['label'])

        print('game_lost: ', self.game_lost)
        print('game_won: ', self.game_won)
        print('_____ran summary_____')

    def deal_piles(self):

        if len(self.deck) == 52:
            # TO DO:  rewrite this to use getattr() and loop through?
            self.pile1.append(self.deck.pop(0))
            for pile in self.hidden_piles[1:]:
                pile.append(self.deck.pop(0))

            self.pile2.append(self.deck.pop(0))
            for pile in self.hidden_piles[2:]:
                pile.append(self.deck.pop(0))

            self.pile3.append(self.deck.pop(0))
            for pile in self.hidden_piles[3:]:
                pile.append(self.deck.pop(0))

            self.pile4.append(self.deck.pop(0))
            for pile in self.hidden_piles[4:]:
                pile.append(self.deck.pop(0))

            self.pile5.append(self.deck.pop(0))
            for pile in self.hidden_piles[5:]:
                pile.append(self.deck.pop(0))

            self.pile6.append(self.deck.pop(0))
            for pile in self.hidden_piles[6:]:
                pile.append(self.deck.pop(0))

            self.pile7.append(self.deck.pop(0))
        else:
            print('Error: deck not full.')
# test out
            # for pile in hidden_piles:
            #     print((pile))
            # for pile in piles:
            #     print((pile))
            # for card in self.pile7_hidden:
            #     print(card['label'])
            # print(self.pile7_hidden)
            print('_____ran deal_piles_____')

    def move_king_to_empty_pile(self):
        moved = False
        # this should be second to flip up card, to possibly pick better king
        pass

    def move_aces_to_suit_pile(self):
        moved = False
        # 1. high priority move, always good idea.
        # 2. check new obj attr aces_complete
        # 3. not sure this makes sense... just add alt logic in suitpile
        #    move that calls it a match if val == targetval + 1
        #    OR if this is an ace.

    def move_to_suitpile(self):
        moved = False
        # 1. check that target pile(-1) or playpile (-1) can play onto an
        # existing suit pile.
        pass

    def move_suitpile_back_to_pile(self):
        moved = False
        # 1. check that a suitpile(-1) could be played
        # onto a pile(-1), AND check if playpile(-1) or any pile(0)
        # (other than pile of target) could be played on the number/color
        # of that suitpile(-1)
        # 2. move card.
        # 3. very LOW (last?)
        pass

    def flip_top_hidden_card(self):
        moved = False
        pile_index = 0
        for pile in self.piles:
            if len(pile) == 0:
                if len(self.hidden_piles[pile_index]) > 0:
                    flipped_card = self.hidden_piles[pile_index][-1]
                    pile.append(self.hidden_piles[pile_index].pop())
                    logging.debug('{}) Flipped up {} on pile {}.'
                                  .format(self.move_number,
                                          flipped_card['label'],
                                          pile_index + 1))
                    moved = True
                    print('ran: flip_top_hidden_card')
            pile_index += 1
        return moved

    def move_pile_to_pile(self):

        candidate_list = []
        # check for candidates
        candidate_pile_index = 0
        candidate = None
        for pile in self.piles:
            if len(pile) > 0:
                candidate = pile[0]
            # check for targets
            target_pile_index = 0
            target = None
            for target_pile in self.piles:
                if ((target_pile_index != candidate_pile_index)
                        & (len(target_pile) > 0)):
                    target = target_pile[-1]
                    if ((candidate['value'] == target['value']-1)
                            & (candidate['color'] != target['color'])):
                        candidate_list.append((
                            candidate_pile_index,
                            target_pile_index,
                            # num cards removing this would candidate uncover
                            len(self.hidden_piles[candidate_pile_index])))
                target_pile_index += 1
            candidate_pile_index += 1
        candidate_list = sorted(candidate_list, key=lambda x: x[2],
                                reverse=True)

        # pick best candidate by # cards uncovered or return false
        if len(candidate_list) > 0:
            chosen_move = candidate_list[0]
            from_pile = chosen_move[0]
            to_pile = chosen_move[1]
            from_card = self.piles[from_pile][0]
            to_card = self.piles[to_pile][-1]
            self.piles[to_pile] = self.piles[to_pile] + self.piles[from_pile]
            self.piles[from_pile].clear()
            logging.debug('{}) Moved {} from pile {} to {} on pile {}.'
                          .format(self.move_number, from_card['label'],
                                  from_pile + 1, to_card['label'],
                                  to_pile + 1))
            moved = True
            print('ran: move_pile_to_pile')
        else:
            # print('No candidates')
            moved = False

        return moved

    def move_playpile_to_piles(self):
        moved = False
        if len(self.play_pile) > 0:
            if self.card_playable(self.play_pile[-1]):
                print('ran: move playpile to piles')
                # bmarkley: TODO
                moved = True
                pass
            else:
                moved = False
        # 1. check if playpile(-1)
        return moved

    def card_playable(self, card):
        playable = False
        if card['value'] == 1:  # this is an Ace
            playable = True
            return playable
        pile_targets = [pile[-1] for pile in self.piles if len(pile) > 0]
        suit_targets = [pile[-1] for pile in self.suit_piles if len(pile) > 0]
        # print('ran: card_playable')
        for target in pile_targets:
            if ((card['value'] == target['value'] - 1)
                    & (card['color'] != target['color'])):
                playable = True
                # print('target', target['label'])
                return playable
        for target in suit_targets:
            if ((card['value'] == target['value'] + 1)
                    & (card['suit'] == target['suit'])):
                playable = True
                # print('suittarget', target['label'])
                return playable
        return playable

    def move_deck_to_playpile(self):
        # move until find a playable card, OR exhaust cards without finding a
        # playable card, in which case game is LOST.
        moved = False
        playable = False
        deck_refilled = False
        while not playable:
            # refill empty deck from playpile if necessary
            if ((len(self.deck) == 0) & (len(self.play_pile) > 0)):
                # unless already refilled once
                if deck_refilled:
                    self.game_lost = True
                    print('Deck exhausted. Game lost.')
                    return moved
                else:
                    self.deck = self.deck + self.play_pile
                    self.play_pile.clear()
                    deck_refilled = True
                    print('ran: swapped playpile back to deck')
                    logging.debug(
                        '{}) Reset {} cards from play_pile back to deck.'
                        .format(self.move_number, len(self.deck)))
            # or just deal out cards onto the playpile
            elif len(self.deck) > 0:
                num_cards = min(3, len(self.deck))
                card_played = 1
                while card_played <= num_cards:
                    self.play_pile.append(self.deck.pop(0))
                    card_played += 1
                moved = True
                playable = self.card_playable(self.play_pile[-1])

                print('ran: move_deck_to_playpile')
                logging.debug('{}) Moved {} cards ({}) from deck to play_pile.'
                              .format(self.move_number, num_cards,
                                      [card['label'] for card in
                                       self.play_pile[-num_cards:]]))
        return moved

    def play_move(self):
        # try moves in order of preference
        moved = False
        move_list = ['flip_top_hidden_card', 'move_pile_to_pile',
                     'move_playpile_to_piles', 'move_deck_to_playpile']
        for move in move_list:
            if ((not moved) & (not self.game_lost)):
                # if deck spins during 'move_deck_to_playpile', will mark lost
                this_move = getattr(self, move)
                moved = this_move()
            else:
                return

    def play_moves(self, max_moves=1):

        while not (self.game_won | self.game_lost):
            self.move_number += 1
            if self.move_number > max_moves:
                print('\nError: reached max_moves. Current max_moves = {}'
                      .format(max_moves))
                self.game_lost = True
            else:
                self.play_move()

        logging.debug('_____ran play_moves_____. num_moves = {}'
                      .format(self.move_number - 1))
        # logging.info, logging.warning
        print('_____ran play_moves_____')


def main(numdecks):

    decks = create_random_deck_indexes(numdecks)

    game = SolitaireGame(decks[0])
    game.deal_piles()
    # game.deck = game.deck[-2:]
    game.play_moves(6)
    game.summary()

    print('_____ran main_____')


if __name__ == "__main__":
    main(numdecks=8)

    # print(len(game.deck))
    # for card in game.deck:
    #     print(card['label'])
    # game.pile7[0]['value'] = 12
    # game.pile7[0]['label'] = 'Q_D'
    # game.pile7[0]['color'] = 'Red'
    # game.pile7[0]['suit'] = 'D'
    # game.pile1[0]['suit'] = 'D'
    # game.pile1[0]['label'] = 'K_D'
    # game.pile1[0]['color'] = 'Red'
    # game.pile7.pop()
    # print(game.pile7_hidden)

    # card = {'label': '6_C', 'value': 6, 'color': 'Red', 'suit': 'C'}
    # cardplayable = game.card_playable(card)
    # print(cardplayable)
