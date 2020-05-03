'''Does this show up in the HELP menu?'''
import random
import logging
import argparse
logging.basicConfig(filename='winning_deck_moves.log', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--mode",
                    help="options are \'single\' or \'bulk\' (default \'bulk\')",
                    default='bulk')
parser.add_argument("--max_moves",
                    help="max number of moves to play (default 220)",
                    type=int, default=220)
parser.add_argument("--num_decks",
                    help="number of decks to create (default 1000)",
                    type=int, default=1000)
parser.add_argument("--deck", help="which single deck to run (default 0)",
                    type=int, default=0)
parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("--factory_deck_columns", help="flip columns->values "
                    "in output", action="store_true")
args = parser.parse_args()


def prune_logfile():
    with open('winning_deck_moves.log') as f:
        listify = []
        for line in f:
            listify.append(line)
    with open('winning_deck_moves.log', 'w') as f:
        tot_length = len(listify)
        listify = listify[-(min(tot_length, 1)):]
        for line in listify:
            f.write(line)


def create_random_deck_indexes(n=5):
    index = [i for i in range(1, 53)]
    indicies = []
    j = 0
    while j < n:
        random.seed(j)
        randindex = index.copy()
        random.shuffle(randindex)
        indicies.append(randindex)
        j += 1

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
    cardindex52 = [int for int in range(1, 53)]

    deck = [list(item) for item in
            zip(labels52, cardvals52, colors52, suits52, cardindex52)]

    # print('deck: {}'.format(deck))


class SolitaireGame:

    suit_index = {'S': 0, 'C': 1, 'H': 2, 'D': 3}

    def __init__(self, randindex, decknum=0, verbose=False,
                 factory_deck_columns=False):

        if verbose:
            print('randindex: {}'.format(randindex))
        deck = []
        if factory_deck_columns:  # features will reflect specific card labels.
            i = 0
            for item in Base.deck:
                deck.append(item + [randindex[i]])
                i += 1
            deck = sorted(deck, key=lambda x: x[5])
        else:  # features will reflect locations in each shuffled deck.
            for index in randindex:
                card = list(filter(lambda x: x[4] == index, Base.deck))[0]
                deck.append(card)

        deck = list(
            map(lambda x: {'label': x[0], 'value': x[1],
                           'color': x[2], 'suit': x[3]}, deck))
        self.deck = deck
        self.decknum = decknum
        self.spade_pile = []
        self.club_pile = []
        self.heart_pile = []
        self.diamond_pile = []
        self.pile1 = []
        self.pile1_hidden = []  # created to simplify indexing. remains empty.
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
        self.suit_piles = [self.spade_pile, self.club_pile,
                           self.heart_pile, self.diamond_pile]
        self.hidden_piles = [self.pile1_hidden, self.pile2_hidden,
                             self.pile3_hidden, self.pile4_hidden,
                             self.pile5_hidden, self.pile6_hidden,
                             self.pile7_hidden]
        self.piles = [self.pile1, self.pile2, self.pile3,
                      self.pile4, self.pile5, self.pile6, self.pile7]
        self.play_pile = []
        self.play_piles = [self.play_pile]  # created to simplify indexing.
        self.game_lost = False
        self.game_won = False
        self.move_number = 0
        self.verbose = verbose
        self.randindex = randindex

# Core:

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
        print('# in deck: {}'.format(len(self.deck)))
        print('game_lost: ', self.game_lost)
        print('game_won: ', self.game_won)
        print('num moves: {}'.format(self.move_number))
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

    def play_move(self):
        # try moves in order of preference
        moved = False
        move_list = ['flip_top_hidden_card', 'move_pile_to_pile',
                     'move_playpile_to_piles', 'back_play',
                     'move_pile_to_suitpile', 'move_partial_pile',
                     'move_deck_to_playpile']
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
                if self.verbose:
                    print('Game won.')
                logging.debug('** Game WON **')
            elif self.move_number > max_moves:
                logging.debug(
                    '\nError: reached max_moves. Current max_moves = {}'.
                    format(max_moves))
                if self.verbose:
                    print('\nError: reached max_moves. Current max_moves = {}'
                          .format(max_moves))
                self.game_lost = True
            else:
                self.play_move()

        logging.debug('_____ran play_moves_____. num_moves = {}'
                      .format(self.move_number - 1))
        if self.verbose:
            print('_____ran play_moves_____')

# Moves:

    def move_pile_to_suitpile(self):

        moved = False
        moves = []
        candidates = self.get_candidates('pile-1th')
        targets = self.get_targets('suit_piles')
        for candidate in candidates:
            num_cards = len(self.hidden_piles[candidate['pile_index']])
            len_pile = len(self.piles[candidate['pile_index']])
            if len_pile > 1:
                num_cards = 0
            for target in targets:
                if self.playable(candidate, target, 'suit'):
                    if not self.deferred(candidate):
                        moves.append(
                            {'candidate': candidate['label'],
                             'candidate_pile': candidate['pile_index'],
                             'candidate_card_index': candidate['card_index'],
                             'cards_uncovered': num_cards,
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
            if self.verbose:
                print('ran: moved pile to suitpile')
            logging.debug('{}) Moved {} from pile {} to {} pile.'.
                          format(self.move_number, move['candidate'],
                                 pile_idx, move['target_suit']))
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
                    if self.verbose:
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
            for suittarget in suittargets:
                num_hidden = 0
                if self.playable(suitcandidate, suittarget, 'suit'):
                    num_hidden = \
                        len(self.hidden_piles[suitcandidate['pile_index']])
                    cards_uncovered_by_suit_play = \
                        max(cards_uncovered_by_suit_play, num_hidden)
                    if len(self.piles[suitcandidate['pile_index']]) > 1:
                        cards_uncovered_by_suit_play = 0  # only 0th uncovers
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
                if self.verbose:
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
                                & (self.playable(candidate, target, 'pile'))
                                & (cards_uncovered >=
                                   cards_uncovered_by_suit_play)):
                            if not self.deferred(candidate):
                                moves.append(
                                    {'candidate': candidate['label'],
                                     'candidate_pile': candidate['pile_index'],
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
            if self.verbose:
                print('ran: move_pile_to_pile')
        else:
            if self.verbose:
                print('No candidates w/ len > suitplay')
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
                        if self.verbose:
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
                    if self.verbose:
                        print('ran: move playpile to suitpile (ace)')
                    return moved
                else:
                    pile_targets = self.get_targets('piles')
                    suit_targets = self.get_targets('suit_piles')
                    for target in pile_targets:
                        if self.playable(card, target, 'pile'):
                            moves.append({'target_type': 'pile',
                                          'target': target['label'],
                                          'target_pile': target['pile_index'],
                                          'target_card_index':
                                          target['card_index']
                                          })
                    for target in suit_targets:
                        if self.playable(card, target, 'suit'):
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
                        if self.verbose:
                            print('ran: moved_playpile_to_piles')
                        return moved
            else:
                moved = False
                if self.verbose:
                    print('ran: moved_pp2p. card not playable')
        return moved

    def move_deck_to_playpile(self):
        # move until find a playable card, OR exhaust cards without finding a
        # playable card, in which case game is LOST.
        moved = False
        playable = False
        deck_refilled = False
        while not playable:
            if ((len(self.deck) == 0) & (len(self.play_pile) == 0)):
                self.game_lost = True
                moved = True
                if self.verbose:
                    print('Deck exhausted. Game lost.')
                logging.debug('{}) Deck exhausted. Game lost.'.
                              format(self.move_number))
                return moved
            # refill empty deck from playpile if necessary
            elif ((len(self.deck) == 0) & (len(self.play_pile) > 0)):
                # unless already refilled once
                if deck_refilled:
                    # put additional any_desperados boolean here
                    self.game_lost = True
                    moved = True
                    if self.verbose:
                        print('Deck exhausted. Game lost.')
                    logging.debug('{}) Deck exhausted. Game lost.'.
                                  format(self.move_number))
                    return moved
                else:
                    # warning: should concatenation be replaced by append/pop?
                    self.deck = self.deck + self.play_pile
                    self.play_pile.clear()
                    deck_refilled = True
                    if self.verbose:
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

                if self.verbose:
                    print('ran: move_deck_to_playpile')
                logging.debug('{}) Moved {} cards ({}) from deck to play_pile.'
                              .format(self.move_number, num_cards,
                                      [card['label'] for card in
                                       self.play_pile[-num_cards:]]))
        return moved

    def move_partial_pile(self):
        moved = False
        candidates = self.get_candidates('pile_deep')
        suit_targets = self.get_targets('suit_piles')
        pile_targets = self.get_candidates('pile-1th')
        suit_moves = []
        for candidate in candidates:
            for suit_target in suit_targets:
                if self.playable(candidate, suit_target, 'suit'):
                    suit_moves.append(
                        {'label': candidate['label'],
                         'value': candidate['value'],
                         'color': candidate['color'],
                         'suit': candidate['suit'],
                         'pile': candidate['pile_index'],
                         'index': candidate['card_index']
                         })
        approved_moves = []
        for suit_move in suit_moves:
            for pile_target in pile_targets:
                if ((suit_move['value'] == pile_target['value']) &
                        (suit_move['color'] == pile_target['color'])):
                    cards_uncovered = \
                        len(self.hidden_piles[suit_move['pile']])
                    if suit_move['index'] > 0:  # must be 0th card
                        cards_uncovered == 0
                    suit_move['alt_label'] = pile_target['label']
                    suit_move['alt_pile'] = pile_target['pile_index']
                    suit_move['cards_uncovered'] = cards_uncovered
                    approved_moves.append(suit_move)
        approved_moves = sorted(approved_moves,
                                key=lambda x: x['cards_uncovered'],
                                reverse=True)
        if len(approved_moves) > 0:
            move = approved_moves[0]
            from_pile = move['pile']
            to_pile = move['alt_pile']
            idx = move['index'] + 1  # poz of card AFTER candidate
            card_after = self.piles[from_pile][idx]['label']
            num_to_move = len(self.piles[from_pile]) - (move['index'] + 1)
            for _ in range(num_to_move):
                self.piles[to_pile].append(self.piles[from_pile].pop(idx))
            moved = True
            if self.verbose:
                print('ran: moved partial pile')
            logging.debug(
                '{}) Moved {} from {} on pile {} to {} on pile {}.'.
                format(self.move_number, card_after, move['label'],
                       move['pile'], move['alt_label'], move['alt_pile']))
        return moved

    def back_play(self, candidate={}):
        # TO DO: only works for playpile. Add support for pile candidates!
        moved = False
        verify = False
        candidates = []
        kings = []

        if candidate != {}:
            # add candidate to list to sync w/ candidate logic below
            candidates.append(candidate)
            verify = True
        else:
            # add a.) playpile, b.) column 'openers' if any needy kings,
            #     c.) uncoverers
            if len(self.play_pile) > 0:
                playpile_candidate = self.get_candidates('play_pile')[0]
                candidates.append(playpile_candidate)
                if playpile_candidate['value'] == 13:
                    kings.append(playpile_candidate)

            pile_kings = self.get_candidates('pile-1th')
            pile_kings = list(filter(lambda x: x['value'] == 13, pile_kings))
            pile_kings = list(filter(
                lambda x: len(self.hidden_piles[x['pile_index']]) > 0,
                pile_kings))
            kings.extend(pile_kings)

            if len(kings) > 0:
                candidates.extend(self.get_candidates('column_openers'))

            uncoverers = self.get_candidates('pile0th')
            uncoverers = list(filter(
                lambda x: len(self.hidden_piles[x['pile_index']]) > 0,
                uncoverers))
            candidates.extend(uncoverers)

        if len(candidates) == 0:
            moved = False
            return moved

        backmovers = self.get_candidates('suitpile_deep')
        open_columns = self.get_targets('open_column')

        worth_trying = False
        for candidate in candidates:
            for backmover in backmovers:
                if self.playable(candidate, backmover, 'pile'):
                    worth_trying = True

        move_queue = []
        local_backmovers = []
        if worth_trying:
            for candidate in candidates:
                local_backmovers = self.get_candidates('suitpile_deep')
                move_queue.clear()
                targets = self.get_candidates('pile-1th')
                # add targets for Kings
                for column in open_columns:
                    targets.append({
                        'candidate_type': column['target_type'],
                        'pile_index': column['pile_index'],
                        'card_index': column['card_index'],
                        'label': column['label'],
                        'value': 14,  # to allow King to play on it naturally
                        'color': 'na',
                        'suit': 'na'
                    })
                target_queue = []
                for i, backmover in enumerate(local_backmovers):
                    backmovers_in_pile = list(filter(
                        lambda x: x['pile_index'] == backmover['pile_index'],
                        local_backmovers))
                    free_card_index = max(
                        [item['card_index'] for item in backmovers_in_pile])
                    card_free = backmover['card_index'] == free_card_index
                    if not card_free:
                        continue
                    target_queue.clear()
                    for j, target in enumerate(targets):
                        if self.playable(backmover, target, 'pile'):
                            target_queue.append(
                                {'bm_pile': backmover['pile_index'],
                                 'bm_card': backmover['card_index'],
                                 'bm_label': backmover['label'],
                                 'bm_value': backmover['value'],
                                 'bm_color': backmover['color'],
                                 'bm_suit': backmover['suit'],
                                 'target_pile': target['pile_index'],
                                 'target_label': target['label'],
                                 'target_index': j
                                 })

                    if len(target_queue) > 0:
                        move = target_queue[0]
                        move_queue.append(move)
                        backmover['pile_index'] = \
                            targets[move['target_index']]['pile_index']
                        targets[move['target_index']] = backmover.copy()
                        # leave backmover in backmovers for indexing but mangle
                        local_backmovers[i]['card_index'] = -999
                        local_backmovers[i]['pile_index'] = -999

                        if self.playable(candidate, backmover, 'pile'):
                            if verify:
                                # return True to card_playable func to
                                # stop dealing
                                return True
                            for move in move_queue:
                                from_pile = move['bm_pile']
                                to_pile = move['target_pile']
                                self.piles[to_pile].append(
                                    self.suit_piles[from_pile].pop(-1))
                                logging.debug(
                                    '{}) Reversed {} from suits to {} on\
                                     pile {}'.
                                    format(self.move_number,
                                           move['bm_label'],
                                           move['target_label'],
                                           move['target_index']
                                           ))
                            if self.verbose:
                                print('ran: backplay cards')
                            moved = True
                            break
        return moved

# Utilities

    def get_candidates(self, type):
        candidates = []
        card_index = 0

        if type == 'pile_deep':
            piles = self.piles
            for index, pile in enumerate(piles):
                len_pile = len(pile)
                if len_pile > 0:  # not top card
                    for card_index, card in enumerate(pile):
                        if card_index < len_pile - 1:
                            candidates.append({'candidate_type': type,
                                               'pile_index': index,
                                               'card_index': card_index,
                                               'pile_len': len_pile,
                                               'label': card['label'],
                                               'value': card['value'],
                                               'color': card['color'],
                                               'suit': card['suit']})

        elif type == 'suitpile_deep':
            piles = self.suit_piles
            for index, pile in enumerate(piles):
                len_pile = len(pile)
                for card_index, card in enumerate(pile):
                    candidates.append({'candidate_type': type,
                                       'pile_index': index,
                                       'card_index': card_index,
                                       # 'pile_len': len_pile,
                                       'label': card['label'],
                                       'value': card['value'],
                                       'color': card['color'],
                                       'suit': card['suit']})
            if len(candidates) > 0:
                candidates = sorted(candidates,
                                    key=lambda x: x['value'],
                                    reverse=True)

        elif type == 'column_openers':
            piles = self.piles
            candidates = self.get_candidates('pile0th')
            candidates = list(filter(
                lambda x: len(self.hidden_piles[x['pile_index']]) == 0,
                candidates))
            candidates = list(filter(
                lambda x: x['value'] != 13,
                candidates))

        else:
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
        # should get RID of this in favor of get_candidates for all calls
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
            return playable
        if card['value'] == 13:
            # check for open column
            for i in range(7):
                if ((len(self.piles[i]) == 0)
                        & (len(self.hidden_piles[i]) == 0)):
                    playable = True
                    return playable
            # if none, look for 'openable' column of a play we've deferred
            deferred = self.get_candidates('pile0th')
            deferred = list(filter(lambda x: not x['value'] == 13, deferred))
            deferred = list(filter(lambda x: not self.deferred(x), deferred))

            def deferred_can_play(card):
                return ((self.card_playable(card, suitpiles=False)) |
                        ((len(self.piles[card['pile_index']]) == 1) &
                         (self.card_playable(card))))
            deferred = list(filter(
                lambda x: deferred_can_play(x),
                deferred))

            if len(deferred) > 0:
                playable = True
                return playable

        pile_targets = self.get_targets('piles')
        for target in pile_targets:
            if self.playable(card, target, 'pile'):
                playable = True
                return playable
        # allow exclusion of suitpiles for move suitpiles to piles
        if suitpiles:
            suit_targets = self.get_targets('suit_piles')
            for target in suit_targets:
                if self.playable(card, target, 'suit'):
                    playable = True
                    return playable
        if not playable:
            # back_play with a candidate returns boolean
            playable = self.back_play(card)

        return playable

    def playable(self, candidate, target, type):
        playable = False
        if type == 'suit':
            if ((candidate['value'] == target['value'] + 1) &
                    (candidate['suit'] == target['suit'])):
                playable = True
        elif type == 'pile':
            if ((candidate['value'] == target['value'] - 1) &
                    (candidate['color'] != target['color'])):
                playable = True
        return playable

    def deferred(self, candidate):
        # false IF: (either ace or two), (not a column clearing move), (makes a
        # valuable move possible), (opens a column for a needy King), (all
        # lower val cards are already suited)
        deferred = True
        # aces and twos never deferred
        if candidate['value'] < 3:
            deferred = False
            return deferred

        pindex = candidate['pile_index']
        cards_hidden = len(self.hidden_piles[pindex])
        # note: suitplay candidates must have pile len == 1. fix later.
        col_clearer = ((candidate['card_index'] == 0) &
                       (cards_hidden == 0))
        if not col_clearer:
            deferred = False
            return deferred
        else:
            # 1st check if all potential dependent cards are suited already
            suited = self.get_candidates('suitpile_deep')
            num_lower_dependent_suited = len(list(filter(
                lambda x: ((x['value'] == candidate['value'] - 1) &
                           (x['color'] != candidate['color'])),
                suited)))
            num_twolower_samecolor_suited = len(list(filter(
                lambda x: ((x['value'] == candidate['value'] - 2) &
                           (x['color'] == candidate['color']) &
                           (x['suit'] != candidate['suit'])),
                suited)))
            if ((num_lower_dependent_suited == 2) &
                    (num_twolower_samecolor_suited == 1)):
                deferred = False
                return deferred
            # a king not on its own column needs a free column
            candidates = self.get_candidates('pile0th')
            kings = list(filter(
                lambda x: ((x['value'] == 13) &
                           (len(self.hidden_piles[x['pile_index']]) > 0)),
                candidates))
            play_pile = self.get_candidates('play_pile')
            if len(play_pile) > 0:
                play_card = play_pile[0]
                if play_card['value'] == 13:
                    kings.append(play_card)
            if len(kings) > 0:
                deferred = False
                return deferred
            # TO DO: add support for 'chainplay'. Single candidate on blank
            # column shouldn't be deferred if playing it allows a meaningful
            # subsequent play.
        return deferred

        logging.debug('cand: {}, piles: {}, msg: {}'.
                      format(candidate['label'], len(self.piles), deferred))


def main(numdecks):
    type = args.mode
    # 'single'  # bulk single testing

    if type == 'single':
        prune_logfile()
        decks = create_random_deck_indexes(numdecks)
        i = args.deck
        game = SolitaireGame(decks[i], i, verbose=args.verbose,
                             factory_deck_columns=args.factory_deck_columns)
        print('Init Deck: {}'.format([card['label'] for card in game.deck]))
        game.deal_piles()
        game.play_moves(args.max_moves)
        game.summary()

    elif type == 'bulk':
        prune_logfile()
        logging.getLogger().setLevel(logging.INFO)  # set lower when in bulk
        decks = create_random_deck_indexes(numdecks)

        results = []
        for i, deck in enumerate(decks):
            game = SolitaireGame(
                deck, i, factory_deck_columns=args.factory_deck_columns)
            game.deal_piles()
            game.play_moves(args.max_moves)
            result = {'decknum': i,
                      'won': game.game_won,
                      'num_moves': game.move_number,
                      'randindex': game.randindex}
            results.append(result)

        tot_decks = len(results)
        won_decks = len(list(filter(lambda x: x['won'], results)))
        num_moves = sum([item['num_moves'] for item in results])

        print('tot_decks, won_decks, won_pct, num_moves, avg_moves')
        print('{:,} {:,} {:.1%} {:,} {:.1f}'.
              format(tot_decks, won_decks, won_decks / tot_decks, num_moves,
                     num_moves/tot_decks))

        with open('winning_deck_results.csv', 'w') as f:
            card_labels = ''
            for index in range(51):
                card_labels += 'x'+str(index)+','
            card_labels += 'x51'
            f.write('deck,num_moves,won,' + card_labels + '\n')

            for result in results:
                card_vals = ''
                for index in result['randindex']:
                    card_vals += str(index) + ','
                card_vals = card_vals[0:len(card_vals)-1]
                line = '{}, {}, {}, {}'.format(result['decknum'],
                                               result['num_moves'],
                                               result['won'],
                                               card_vals)
                f.write(line + '\n')
        msg = '"winning_deck_results.csv" written to local dir '\
              'with {} rows.'
        print(msg.format(tot_decks))

    elif type == 'testing':
        prune_logfile()
        decks = create_random_deck_indexes(1)
        i = 0
        game = SolitaireGame(decks[i], i, verbose=False)
        game.deck.clear()
        game.diamond_pile.append(
            {'label': '5_D', 'value': 5, 'color': 'Red', 'suit': 'D'})
        game.pile1.append(
            {'label': 'K_S', 'value': 13, 'color': 'Black', 'suit': 'S'})
        game.pile2.append(
            {'label': 'K_C', 'value': 13, 'color': 'Black', 'suit': 'C'})
        game.pile2_hidden.append(
            {'label': 'J_C', 'value': 11, 'color': 'Black', 'suit': 'C'})
        game.pile7.append(
            {'label': '8_H', 'value': 8, 'color': 'Red', 'suit': 'H'})
        game.deck.append(
            {'label': '10_H', 'value': 10, 'color': 'Red', 'suit': 'H'})
        game.play_pile.append(
            {'label': '3_C', 'value': 3, 'color': 'Black', 'suit': 'C'})

        game.play_moves(3)
        game.summary()

    print('_____ran main_____')


if __name__ == "__main__":
    main(numdecks=args.num_decks)
