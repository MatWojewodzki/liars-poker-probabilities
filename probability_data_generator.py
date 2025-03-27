from hand_probability import DeckInfo, HandProbability
import numpy as np
from itertools import repeat, product
import json


OUTPUT_FILE_NAME: str = "probability_data.json"
DIGITS_OF_PRECISION: int | None = 6
PRETTIFY: bool = False


def list_of_probabilities(selected_cards: np.ndarray, func: callable):
    return np.vectorize(func)(selected_cards).tolist()


def main():
    deck_info = DeckInfo(deck_size=24, cards_of_rank_count=4, cards_of_suit_count=6)
    hand_probability = HandProbability(deck_info, digits_of_precision=DIGITS_OF_PRECISION)

    selected_cards = np.arange(1, deck_info.deck_size)

    probability_data = {
        "rank": {
            f"{i}+{j}": list_of_probabilities(selected_cards, hand_probability.at_least_of_ranks_probability_function(i, j))
            for i, j in product(range(1, 4), range(0, 3)) if i >= j
        } | {
            "4+0": list_of_probabilities(selected_cards, hand_probability.at_least_of_ranks_probability_function(4))
        },
        "street": {
            str(i): list_of_probabilities(selected_cards, hand_probability.at_least_of_ranks_probability_function(*repeat(1, i)))
            for i in range(1, 6)
        },
        "flush": {
            str(i): list_of_probabilities(selected_cards, hand_probability.at_least_of_suits_probability_function(i))
            for i in range(1, 6)
        },
        "straight_flush": {
            str(i): list_of_probabilities(selected_cards, hand_probability.unique_cards_probability_function(i))
            for i in range(1, 6)
        }
    }

    indent = 4 if PRETTIFY else None
    with open(OUTPUT_FILE_NAME, "w") as f:
        json.dump(probability_data, f, indent=indent)


if __name__ == '__main__':
    main()