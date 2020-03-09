
Winning Deck: Analysis with Tensorflow and AdaBoostRegressor - Brian Markley

Predict Winning Solitaire Decks with Tensorflow and AdaBoostRegressor.

Given that some shuffled decks will win and some will lose in a game of solitaire (aka Klondike), can we generalize features of WINNING DECKS and predict if a newly shuffled deck will win? OR, are there so many possible winning decks and move-orders that patterns in the winning training decks could never generalize to unseen decks?
Process:

I created a Solitaire class in python to play 10,000 games of solitaire and produce training data with a card ID (1-52) for each of the 52 locations in a shuffled deck (e.g. x0 = top card, x51 = bottom card), a won flag (true|false), and the num_moves (1-156) played until the deck was either won or lost. I produced an alternate data set where the 52 card features represented specific cards (e.g. x0 = 2-of-Spades, x51 = Ace-of-Hearts, with cell values giving the shuffled deck locations), but this yielded very similar results.

Below, after basic exploration, I trained a classifier to target the won column and a regressor to target the correlated num_moves column using various column subsets, data transformations, and new statistical features. Although I am new to deep models, I thought it would be best to try one here since I'd expect any function to be very non-linear.
Conclusions:

I found no way to identify winning decks. Although a trained tensorflow classifier could fully memorize the 7500 training decks and correctly classify 100% of samples pulled from within, it could not generalize to new decks. As a final gut-check, I added in a noise-degraded copy of the num_moves feature to the training data and showed 99% accuracy in classification.

It appears winning decks use a sufficiently complex series of moves (usually more than 115) such that their initial states are indistinguishable from those of losing decks. This agrees with my experience that the difference between winning and losing often hinges on a single linchpin card appearing at the right time or failing to appear. A winning deck would appear statistically identical to one where only that linchpin card is offset by 1.
Ways to improve this?:

I would love to hear thoughts on whether successful prediction sounds possible, and how I might improve.

Some problems I see are:

    My Solitaire playing algorithm only achieves ~18% success but research shows I should be able to achieve ~43%. If I improve the algorithm, perhaps the wider pool of winnable decks might be more generalizable? Alternatively, since I'm already winning the 'easiest' decks, I might expect this could actually hurt generalizability, since it would add more marginal decks that take more complex game play to win.
    I am new to deep models and am using a simple input layer. Perhaps this problem would lend itself to a differently shaped input layer representing card value, suit, and location for each card, and convolutional filters akin to vision problems?
