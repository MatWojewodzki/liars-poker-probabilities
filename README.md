# liars-poker-probabilities

Python script for calculating the exact probabilities of having any poker
hand (or it's subpart) on the table in a liar's poker card game. Remember these are the probabilities of specific
hands like a "pair of jacks", a "full house of 3 kings and 2 queens" or a "flush of hearts".

## Installation

1. Clone the repository

    ```bash
    git clone https://github.com/MatWojewodzki/liars-poker-probabilities.git
    ```

2. Install the requirements

    ```bash
    pip install -r requirements.txt
    ```

## Usage

There are 2 entry points calculating probability of poker hands assuming a standard 24 card deck with 4 cards
of each rank and 6 cards of each suit:

- run the `probability_data_generator.py` to generate a JSON file containing
  data about all the possible poker hand probabilities including any sub-hands (e.g. a pair and a high card),
- run the `plot_generator.py` to create a plot presenting probability of the poker hands.

You may create your own script to gather data about other hands or the probability in a game with a different
deck size. For this purpose, use the `DeckInfo` and `HandProbability` classes from the `hand_probability.py` module.