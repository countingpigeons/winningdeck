## Winning Deck: Predict Winning Solitaire Decks with Tensorflow and AdaBoostRegressor.

Given that some shuffled decks will win and some will lose in a game of Solitaire (aka Klondike), can we generalize features of winning decks and predict if a newly shuffled deck will win? Or, are there so many possible winning decks and move-orders that patterns in winning training decks could never generalize to unseen decks?

I could not find generalizable differences between winning and losing decks and am not sure this is possible given the huge space of possible shuffled decks and the statistical similarity between hypothetical winning and losing decks where a critical card is offset by a single position. I still found the analysis really interesting, and hope others might too.

Please feel free to contribute improvements in either the Solitaire playing algorithm or the notebook analysis. I'd love to know how others would approach this!

### Contents:
- **winning_deck.py:** An OOP program in 'pure' Python (no libraries except 'logging' and 'random') that plays 10K games of Solitaire and outputs results as training data. 
- **winning_deck_results** 10K rows of training data with a card ID (1-52) for each of the 52 locations in a shuffled deck (e.g. x0 = top card, x51 = bottom card), a won flag (true|false), and the num_moves (1-156) played until the deck was either won or lost.
- **solitaire_analysis.ipynb:** A Jupyter notebook in Python/Pandas with exploratory data analysis and classification attempts with a Tensorflow deep classifier and an AdaBoostRegressor.
