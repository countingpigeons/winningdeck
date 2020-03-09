## Winning Deck: Predict Winning Solitaire Decks with Tensorflow and AdaBoostRegressor.

Given that some shuffled decks will win and some will lose in a game of solitaire (aka Klondike), can we generalize features of WINNING DECKS and predict if a newly shuffled deck will win? OR, are there so many possible winning decks and move-orders that patterns in winning training decks could never generalize to unseen decks?

### Contents:
- **winning_deck.py:** An OOP program in 'pure' Python (no libraries except 'logging' and 'random') that plays 10K games of solitaire and outputs results as training data. 
- **winning_deck_results** 10K rows of training data with a card ID (1-52) for each of the 52 locations in a shuffled deck (e.g. x0 = top card, x51 = bottom card), a won flag (true|false), and the num_moves (1-156) played until the deck was either won or lost.
- **solitaire_analysis.ipynb:** A Jupyter notebook in Python with exploratory data analysis using Pandas and classification attempts with a Tensorflow deep classifier and an AdaBoostRegressor.
