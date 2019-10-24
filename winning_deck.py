import random
import logging
logging.basicConfig(filename='winning_deck_moves.log', level=logging.DEBUG)


def prune_logfile():
    with open('winning_deck_moves.log') as f:
        listify = []
        for line in f:
            listify.append(line)
    with open('winning_deck_moves.log', 'w') as f:
        tot_length = len(listify)
        listify = listify[-(min(tot_length, 20)):]
        for line in listify:
            f.write(line)


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
    suit_index = {'S': 0, 'C': 1, 'H': 2, 'D': 3}
    hidden_piles = [pile1_hidden, pile2_hidden, pile3_hidden, pile4_hidden,
                    pile5_hidden, pile6_hidden, pile7_hidden]
    piles = [pile1, pile2, pile3, pile4, pile5, pile6, pile7]
    play_pile = []
    play_piles = [play_pile]  # created to simplify indexing. always one pile.
    game_lost = False
    game_won = False
    move_number = 0

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
        print('Suit Piles:')
        for pile in self.suit_piles:
            print('Suit_Pile {}:'.format(pile_index), end='')
            if len(pile) > 0:
                print([card['label'] for card in pile])
            else:
                print('na')
            pile_index += 1
        pile_index = 0
        print('Piles:')
        for pile in self.piles:
            print('Pile {}:'.format(pile_index), end='')
            if len(pile) > 0:
                print([card['label'] for card in pile], end='')
            else:
                print('na', end='')
            print(' h: {}'.format(len(self.hidden_piles[pile_index])))
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

            initial_candidates = []
            for pile in self.piles:
                for card in pile:
                    initial_candidates.append(card['label'])
            logging.debug('{}) Initial dealt piles: {}'.
                          format(self.move_number, initial_candidates))
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

    def move_pile_to_suitpile(self):
        # move pile2pile checks if one of these would uncover more cards and
        # fails if so to allow this to run in its place.
        moved = False
        moves = []
        candidates = self.get_candidates('pile-1th')
        targets = self.get_targets('suit_piles')
        for candidate in candidates:
            for target in targets:
                if ((candidate['value'] == target['value'] + 1) &
                        (candidate['suit'] == target['suit'])):
                    moves.append({'candidate': candidate['label'],
                                  'candidate_pile': candidate['pile_index'],
                                  'candidate_card_index':
                                      candidate['card_index'],
                                  'cards_uncovered':
                                      len(self.hidden_piles[
                                          candidate['pile_index']]),
                                  'target': target['label'],
                                  'target_pile': target['pile_index'],
                                  'target_card_index': target['card_index'],
                                  'target_suit': candidate['suit']})
        if len(moves) > 0:
            moves = sorted(moves, key=lambda x: x['cards_uncovered'],
                           reverse=True)
            move = moves[0]
            suit_idx = move['target_pile']
            pile_idx = move['candidate_pile']
            self.suit_piles[suit_idx].append(self.piles[pile_idx].pop(-1))
            moved = True
            print('ran: moved pile to suitpile')
            # print('Moved card to {} suitpile'.format(move['target_suit']))
            logging.debug('{}) Moved {} from pile {} to {} pile.'.
                          format(self.move_number, move['candidate'],
                                 pile_idx, move['target_suit']))
        return moved

    def move_suitpile_back_to_pile(self):
        moved = False
        backmovers = self.get_candidates('suit_piles')
        approved_backmovers = []  # stage backmovers w/ # cards uncoverable
        targets = self.get_targets('piles')
        pile_candidates = self.get_candidates('pile0th')

        for backmover in backmovers:
            if backmover['value'] >= 3:  # aces and twos never useful
                card = {'label': backmover['label'],
                        'value': backmover['value'],
                        'color': backmover['color'],
                        'suit': backmover['suit']}
                if self.card_playable(card, suitpiles=False):
                    for pcandidate in pile_candidates:
                        num_hidden = \
                            len(self.hidden_piles[pcandidate['pile_index']])
                        if ((pcandidate['value'] == backmover['value'] - 1) &
                                (pcandidate['color'] != backmover['color'])):
                            approved_backmovers.append(
                                {'pile': backmover['pile_index'],
                                 'pcandidate': pcandidate['label'],
                                 'num_cards': num_hidden
                                 })
                    if len(self.play_pile) > 0:
                        ppcandidate = self.play_pile[-1]
                        if ((ppcandidate['value'] == backmover['value'] - 1) &
                                (ppcandidate['color'] != backmover['color'])):
                            approved_backmovers.append(
                                {'pile': backmover['pile_index'],
                                 'pcandidate': ppcandidate['label'],
                                 'num_cards': 0
                                 })
        # pick backmover that can uncover the most cards under dependent
        approved_backmovers = sorted(
            approved_backmovers,
            key=lambda x: x['num_cards'],
            reverse=True)
        if len(approved_backmovers) > 0:
            approved_backmove = approved_backmovers[0]
            backmove_card = self.suit_piles[approved_backmove['pile']][-1]
            moves = []
            for target in targets:
                if ((backmove_card['value'] == target['value'] - 1) &
                        (backmove_card['color'] != target['color'])):
                    # warning: dubious sort criteria. think this through.
                    len_target_pile = len(self.piles[target['pile_index']])
                    print('target: {}'.format(target))
                    moves.append({'candidate': backmove_card['label'],
                                  'candidate_pile':
                                  approved_backmove['pile'],
                                  'candidate_card_index': -1,
                                  'len_target_pile': len_target_pile,
                                  'target': target['label'],
                                  'target_pile': target['pile_index'],
                                  'target_card_index': target['card_index']})
            # pick target with smallest pile (dubious). prob distance to its
            # current suitpile max is best. i.e. will it be playable to
            # suitpile soon? if so, play backmover to the other suited card.
            moves = sorted(moves,
                           key=lambda x: x['len_target_pile'],
                           reverse=False)
            if len(moves) > 0:
                move = moves[0]
                from_idx = move['candidate_pile']
                to_idx = move['target_pile']
                self.piles[to_idx].append(self.suit_piles[from_idx].pop(-1))
                print('ran: move suitpile back to pile')
                moved = True
                logging.debug('{}) Moved {} from suitpile {} to {} on pile {}'.
                              format(self.move_number, move['candidate'],
                                     move['candidate'][-1], move['target'],
                                     move['target_pile']))
        return moved

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
                                          pile_index))
                    moved = True
                    print('ran: flip_top_hidden_card')
            pile_index += 1
        return moved

    def move_pile_to_pile(self):
        moved = False
        candidates = self.get_candidates('pile0th')
        targets = self.get_targets('piles')
        kingtargets = self.get_targets('open_column')
        suitcandidates = self.get_candidates('pile-1th')
        suittargets = self.get_targets('suit_piles')
        cards_uncovered_by_suit_play = 0
        for suitcandidate in suitcandidates:
            # len_candidate_pile = len(self.piles[suitcandidate['pile_index']])
            for suittarget in suittargets:
                i = 0
                if ((suitcandidate['value'] == suittarget['value'] + 1) &
                        (suitcandidate['suit'] == suittarget['suit'])):
                    i = len(self.hidden_piles[suitcandidate['pile_index']])
                    cards_uncovered_by_suit_play = \
                        max(cards_uncovered_by_suit_play, i)
        moves = []
        for candidate in candidates:
            cards_uncovered = len(self.hidden_piles[candidate['pile_index']])
            # only consider Kings to move if they will uncover some cards
            if ((candidate['value'] == 13) &
                    (cards_uncovered > 0)):
                for target in kingtargets:
                    moves.append({'candidate': candidate['label'],
                                  'candidate_pile': candidate['pile_index'],
                                  'candidate_card_index':
                                      candidate['card_index'],
                                  'cards_uncovered': cards_uncovered,
                                  'target': target['label'],
                                  'target_pile': target['pile_index'],
                                  'target_card_index': target['card_index']})
            elif candidate['value'] == 1:
                suit_pile = self.suit_index[candidate['suit']]
                from_pile = candidate['pile_index']
                self.suit_piles[suit_pile].append(self.piles[from_pile].pop())
                print('ran: move pile to suitpile (ace)')
                moved = True
                logging.debug('{}) Moved {} from pile {} to {} pile.'.
                              format(self.move_number, candidate['label'],
                                     from_pile, candidate['suit']))
                return moved
            else:
                if cards_uncovered >= cards_uncovered_by_suit_play:
                    for target in targets:
                        if ((candidate['pile_index'] != target['pile_index'])
                                & (candidate['value'] == target['value']-1)
                                & (candidate['color'] != target['color'])
                                & (cards_uncovered >=
                                   cards_uncovered_by_suit_play)):
                            moves.append({'candidate': candidate['label'],
                                          'candidate_pile':
                                          candidate['pile_index'],
                                          'candidate_card_index':
                                              candidate['card_index'],
                                          'cards_uncovered': cards_uncovered,
                                          'target': target['label'],
                                          'target_pile': target['pile_index'],
                                          'target_card_index':
                                          target['card_index']})
            # pick candidate that uncovers the most cards
        moves = sorted(moves, key=lambda x: x['cards_uncovered'], reverse=True)

        if len(moves) > 0:
            chosen_move = moves[0]
            from_pile = chosen_move['candidate_pile']
            to_pile = chosen_move['target_pile']
            while len(self.piles[from_pile]) > 0:
                self.piles[to_pile].append(self.piles[from_pile].pop(0))
            # the below method of concatenating piles does NOT update the
            # pile indexes when running within the play_moves Loop.
            # It IS updated by the time the summary() method runs though!

            # self.piles[to_pile] = self.piles[to_pile] + self.piles[from_pile]
            # self.piles[from_pile].clear()
            logging.debug('{}) Moved {} from pile {} to {} on pile {}.'
                          .format(self.move_number, chosen_move['candidate'],
                                  from_pile, chosen_move['target'],
                                  to_pile))
            moved = True
            print('ran: move_pile_to_pile')
        else:
            # print('No candidates w/ len > suitplay')
            moved = False
        return moved

    def move_playpile_to_piles(self):
        moved = False
        if len(self.play_pile) == 0:
            return moved
        else:
            card = self.play_pile[-1]
            if self.card_playable(card):
                moves = []
                if card['value'] == 13:
                    pile_targets = self.get_targets('open_column')
                    for target in pile_targets:
                        moves.append({'target_type': 'open_column',
                                      'target': 'na',
                                      'target_pile': target['pile_index'],
                                      'target_card_index': 'na'
                                      })
                        move = moves[0]  # doesn't matter which empty pile
                        pile_idx = move['target_pile']
                        pile = self.piles[pile_idx]
                        pile.append(self.play_pile.pop(-1))
                        print('ran: moved playpile King to empty column')
                        moved = True
                        logging.debug('{}) Moved {} from playpile to pile {}.'.
                                      format(self.move_number,
                                             card['label'],
                                             pile_idx))
                        return moved
                elif card['value'] == 1:
                    idx = self.suit_index[card['suit']]
                    self.suit_piles[idx].append(self.play_pile.pop(-1))
                    moved = True
                    logging.debug(
                        '{}) Moved {} from playpile to {} pile.'.
                        format(self.move_number, card['label'], card['suit']))
                    print('ran: move playpile to suitpile (ace)')
                    return moved
                else:
                    pile_targets = self.get_targets('piles')
                    suit_targets = self.get_targets('suit_piles')
                    for target in pile_targets:
                        if ((card['value'] == target['value'] - 1) &
                                (card['color'] != target['color'])):
                            moves.append({'target_type': 'pile',
                                          'target': target['label'],
                                          'target_pile': target['pile_index'],
                                          'target_card_index':
                                          target['card_index']
                                          })
                    for target in suit_targets:
                        if ((card['value'] == target['value'] + 1) &
                                (card['suit'] == target['suit'])):
                            moves.append({'target_type': 'suitpile',
                                          'target': target['label'],
                                          'target_pile': target['pile_index'],
                                          'target_card_index':
                                          target['card_index']
                                          })
                    # prefer pile over suitpile
                    moves = sorted(moves, key=lambda x: x['target_type'])
                    if len(moves) > 0:
                        move = moves[0]
                        pile_idx = move['target_pile']
                        if move['target_type'] == 'pile':
                            pile = self.piles[pile_idx]
                        elif move['target_type'] == 'suitpile':
                            pile = self.suit_piles[pile_idx]
                        pile.append(self.play_pile.pop(-1))
                        moved = True

                        if move['target_type'] == 'pile':
                            logging.debug(
                                '{}) Moved {} from playpile to {} on pile {}.'
                                .format(self.move_number, card['label'],
                                        move['target'], move['target_pile']))
                        elif move['target_type'] == 'suitpile':
                            logging.debug(
                                '{}) Moved {} from playpile to {} pile.'
                                .format(self.move_number, card['label'],
                                        card['suit']))

                        # logging.debug(
                        #     '{}) Moved {} from playpile to {} on pile {}.'
                        #     .format(self.move_number, card['label'],
                        #             move['target'], move['target_pile']))
                        print('ran: moved_playpile_to_piles')
                        return moved
            else:
                moved = False
                # print('card not playable')
        return moved

    def get_candidates(self, type):
        candidates = []
        card_index = 0
        # piles = self.piles

        if type == 'pile0th':
            card_index = 0
            piles = self.piles
        elif type == 'pile-1th':
            card_index = -1
            piles = self.piles
        elif type == 'suit_piles':
            card_index = -1
            piles = self.suit_piles
        elif type == 'play_pile':
            card_index = -1
            piles = self.play_piles

        for index, pile in enumerate(piles):
            if len(pile) > 0:
                candidates.append({'candidate_type': type,
                                   'pile_index': index,
                                   'card_index': card_index,
                                   'label': pile[card_index]['label'],
                                   'value': pile[card_index]['value'],
                                   'color': pile[card_index]['color'],
                                   'suit': pile[card_index]['suit']})
        return candidates

    def get_targets(self, type):
        targets = []
        piles = []

        if type in (['piles', 'suit_piles']):
            if type == 'piles':
                card_index = -1
                piles = self.piles
            elif type == 'suit_piles':
                card_index = -1
                piles = self.suit_piles

            for index, pile in enumerate(piles):
                if len(pile) > 0:
                    targets.append({'target_type': type,
                                    'pile_index': index,
                                    'card_index': card_index,
                                    'label': pile[card_index]['label'],
                                    'value': pile[card_index]['value'],
                                    'color': pile[card_index]['color'],
                                    'suit': pile[card_index]['suit']})

        elif type == 'open_column':
            card_index = 0
            piles = self.piles
            hidden_piles = self.hidden_piles
            for i in range(7):
                if len(piles[i]) == 0 and len(hidden_piles[i]) == 0:
                    targets.append({'target_type': type,
                                    'pile_index': i,
                                    'card_index': card_index,
                                    'label': 'na',
                                    'value': 'na',
                                    'color': 'na',
                                    'suit': 'na'})
        return targets

    def card_playable(self, card, suitpiles=True):
        playable = False

        if card['value'] == 1:  # this is an Ace
            playable = True
            # self.game_lost = True
            return playable
        if card['value'] == 13:
            for i in range(7):
                if ((len(self.piles[i]) == 0)
                        & (len(self.hidden_piles[i]) == 0)):
                    playable = True
                    print('found a King playable')
                    return playable

        pile_targets = self.get_targets('piles')
        for target in pile_targets:
            if ((card['value'] == target['value'] - 1)
                    & (card['color'] != target['color'])):
                playable = True
                return playable
        # allow exclusion of suitpiles for move suitpiles to piles
        if suitpiles:
            suit_targets = self.get_targets('suit_piles')
            for target in suit_targets:
                if ((card['value'] == target['value'] + 1)
                        & (card['suit'] == target['suit'])):
                    playable = True
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
                    moved = True
                    print('Deck exhausted. Game lost.')
                    logging.debug('{}) Deck exhausted. Game lost.'.
                                  format(self.move_number))
                    return moved
                else:
                    # warning: should concatenation be replaced by append/pop?
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
                     'move_pile_to_suitpile', 'move_playpile_to_piles',
                     'move_suitpile_back_to_pile', 'move_deck_to_playpile']
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
            cards_suited = len(self.spade_pile + self.club_pile +
                               self.heart_pile + self.diamond_pile)
            if cards_suited == 52:
                self.game_won = True
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

    prune_logfile()
    decks = create_random_deck_indexes(numdecks)
    game = SolitaireGame(decks[2])
    game.deal_piles()

    # game.pile7_hidden.clear()
    game.play_moves(60)

    # game.pile3.clear()
    # game.pile5.clear()
    # game.pile5_hidden.clear()
    # game.pile3_hidden.clear()

    # card = {'label': 'A_D', 'value': 1, 'color': 'Red', 'suit': 'D'}
    # game.diamond_pile.append(card)
    # card = {'label': 'K_H', 'value': 13, 'color': 'Red', 'suit': 'H'}
    # game.pile7[0] = card
    # card = {'label': '4_S', 'value': 4, 'color': 'Black', 'suit': 'S'}
    # game.pile1[0] = card
    # card2 = {'label': '6_C', 'value': 6, 'color': 'Black', 'suit': 'C'}
    # game.pile6.append(card2)
    # print(game.card_playable(card2))
    game.summary()

    print('_____ran main_____')


if __name__ == "__main__":
    main(numdecks=8)

    # print(len(game.deck))
    # for card in game.deck:
    #     print(card['label'])
    # game.pile1[0]['suit'] = 'D'
    # game.pile1[0]['label'] = 'K_D'
    # game.pile1[0]['color'] = 'Red'
    # game.pile7.pop()
    # print(game.pile7_hidden)

    # card = {'label': '6_C', 'value': 6, 'color': 'Red', 'suit': 'C'}
    # cardplayable = game.card_playable(card)
    # print(cardplayable)

    # game.play_pile.append(game.deck.pop(0))
    # game.heart_pile.append(game.deck.pop(0))
    # game.club_pile.append(game.deck.pop(0))
    # game.spade_pile.append(game.deck.pop(0))

    # game.deck = game.deck[-2:]
    # game.pile7_hidden.pop()
    # game.pile7_hidden.pop()
    # game.pile7_hidden.pop()
    # game.pile7_hidden.pop()
    # game.pile7_hidden.pop()
    #
    # game.pile7[0]['value'] = 12
    # game.pile7[0]['label'] = 'Q_D'
    # game.pile7[0]['color'] = 'Red'
    # game.pile7[0]['suit'] = 'D'

    # def move_aces_or_twos_to_suit_pile(self):
    #     moved = False
    #     candidates = self.get_candidates('pile-1th')
    #     candidates.extend(self.get_candidates('play_pile'))
    #     suit_index = {'S': 0, 'C': 1, 'H': 2, 'D': 3}
    #     # print('play-pile: ', self.get_candidates('play_pile'))
    #     moves = []
    #     for candidate in candidates:
    #         i = suit_index[candidate['suit']]
    #         j = candidate['pile_index']

    # if candidate['value'] == 1:
    #     if candidate['candidate_type'] == 'play_pile':
    #         self.suit_piles[i].append(self.play_pile.pop(-1))
    #     if candidate['candidate_type'] == 'pile-1th':
    #         self.suit_piles[i].append(self.piles[j].pop(-1))
    #     moves.append(candidate)
    #     logging.debug('{}) Moved {} from {}[{}] to {} pile.'.
    #                   format(self.move_number, candidate['label'],
    #                          candidate['candidate_type'],
    #                          j, candidate['suit']))
    #     # print('moves: {}'.format(moves))
    #     # print('suit_pile_index: {}'.format(i))
    #     moved = True
    # print('ran: move ace or two to suitpile (ace)')

    # if candidate['value'] == 2:
    #     if len(self.suit_piles[i]) > 0:  # must already have ace
    #         if candidate['candidate_type'] == 'play_pile':
    #             self.suit_piles[i].append(self.play_pile.pop(-1))
    #         if candidate['candidate_type'] == 'pile-1th':
    #             self.suit_piles[i].append(self.piles[j].pop(-1))
    #         moves.append(candidate)
    #         logging.debug('{}) Moved {} from {}[{}] to {} pile.'.
    #                       format(self.move_number, candidate['label'],
    #                              candidate['candidate_type'],
    #                              j, candidate['suit']))
    #         moved = True
    #         print('ran: move ace or two to suitpile (two)')
    # return moved

    # def move_king_to_empty_pile(self):
    #     moved = False
    #     # this should be second to flip up card, to possibly pick better king
    #     pass
