## Winning Deck: Predict winning Solitaire decks.

Can we generalize features of winning decks in Solitaire and predict if a newly shuffled deck will win? Or, is the initial order of the cards like a fingerprint, and the slightest change in order changes a winning deck into a losing one.

This project creates training data through a custom program to play lots of games of Solitaire, which is then used in a Jupyter Notebook analysis. 

### Contents:
* <b>winning_deck.py:</b> An OOP program in 'pure' Python (no libraries except 'logging' and 'random') that plays 10K games of Solitaire and outputs results to a .csv file.
* <b>winning_deck_results.csv:</b> 10K rows of training data with a card ID (1-52) for each of the 52 locations in a shuffled deck (e.g. x0 = top card, x51 = bottom card), a won flag (true|false), and the num_moves (1-156) played until the deck was either won or lost.
* <b>solitaire_analysis.ipynb:</b> A Jupyter notebook in Python/Pandas with exploratory data analysis and classification with Tensorflow and AdaBoostRegressor.

### Findings:

Although summarized in the attached analysis, the upshot is that I couldn't get a signal from general deck qualities (e.g. the color or value balance of the two halves of the deck, card-value offsets from position to position, how contiguous values were  throughout etc...) leading me to conclude that Solitaire decks are unique and win through precise ordering, not general qualities of the particular shuffle. Please feel free to review and make improvements!
