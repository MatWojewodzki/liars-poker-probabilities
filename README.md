# liars-poker-probabilities

Python API for calculating the exact probabilities of having any poker hand on the table in
liar's poker card game. Remember these are the probabilities of specific hands like a "pair of jacks",
a "full house of 3 kings and 2 queens" or a "flush of hearts".

## Python version

Tested for Python 3.12

## Installation

1. Clone the repository

    ```bash
    git clone https://github.com/MatWojewodzki/liars-poker-probabilities.git
    ```

2. Install the requirements if you intend to run the `plot_generator.py` script.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

The API is located in the `hand_probability.py` module.

In addition, there are 2 scripts calculating probability of poker hands assuming a standard 24 card deck with 4 cards
of each rank and 6 cards of each suit (standard deck from 9 to Ace):

- run the `probability_data_generator.py` to generate a JSON file containing probabilities of all poker hands
  including any sub-hands (e.g. probability of having a pair when one of the cards is already on your hand),
- run the `plot_generator.py` to create a plot presenting the probability of poker hands depending on the number
  of cards randomly selected from the deck.