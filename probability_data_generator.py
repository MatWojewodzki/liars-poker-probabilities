from hand_probability import DeckInfo, HandProbability
import numpy as np
from itertools import repeat
import json


OUTPUT_FILE_NAME: str = "probability_data.json"
DIGITS_OF_PRECISION: int | None = 6


def list_of_probabilities(selected_cards: np.ndarray, func: callable):
    return np.vectorize(func)(selected_cards).tolist()


def main():
    deck_info = DeckInfo(deck_size=24, cards_of_rank_count=4, cards_of_suit_count=6)
    hand_probability = HandProbability(deck_info, digits_of_precision=DIGITS_OF_PRECISION)

    selected_cards = np.arange(1, deck_info.deck_size)

    high_card_func = hand_probability.at_least_of_ranks_probability_function(1)
    pair_func = hand_probability.at_least_of_ranks_probability_function(2)
    three_of_a_kind_func = hand_probability.at_least_of_ranks_probability_function(3)
    four_of_a_kind_func = hand_probability.at_least_of_ranks_probability_function(4)
    two_high_cards_func = hand_probability.at_least_of_ranks_probability_function(1, 1)
    pair_and_high_card_func = hand_probability.at_least_of_ranks_probability_function(2, 1)
    two_pair_func = hand_probability.at_least_of_ranks_probability_function(2, 2)
    three_of_a_kind_and_high_card_func = hand_probability.at_least_of_ranks_probability_function(3, 1)
    full_house_func = hand_probability.at_least_of_ranks_probability_function(3, 2)

    street_of_5_func = hand_probability.at_least_of_ranks_probability_function(*repeat(1, 5))
    street_of_4_func = hand_probability.at_least_of_ranks_probability_function(*repeat(1, 4))
    street_of_3_func = hand_probability.at_least_of_ranks_probability_function(*repeat(1, 3))
    street_of_2_func = hand_probability.at_least_of_ranks_probability_function(*repeat(1, 2))
    street_of_1_func = hand_probability.at_least_of_ranks_probability_function(*repeat(1, 1))

    flush_of_5_func = hand_probability.at_least_of_suits_probability_function(5)
    flush_of_4_func = hand_probability.at_least_of_suits_probability_function(4)
    flush_of_3_func = hand_probability.at_least_of_suits_probability_function(3)
    flush_of_2_func = hand_probability.at_least_of_suits_probability_function(2)
    flush_of_1_func = hand_probability.at_least_of_suits_probability_function(1)

    straight_flush_of_5_func = hand_probability.unique_cards_probability_function(5)
    straight_flush_of_4_func = hand_probability.unique_cards_probability_function(4)
    straight_flush_of_3_func = hand_probability.unique_cards_probability_function(3)
    straight_flush_of_2_func = hand_probability.unique_cards_probability_function(2)
    straight_flush_of_1_func = hand_probability.unique_cards_probability_function(1)

    probability_data = {
        "rank": {
            "1": list_of_probabilities(selected_cards, high_card_func),
            "2": list_of_probabilities(selected_cards, pair_func),
            "3": list_of_probabilities(selected_cards, three_of_a_kind_func),
            "4": list_of_probabilities(selected_cards, four_of_a_kind_func),
            "1+1": list_of_probabilities(selected_cards, two_high_cards_func),
            "2+1": list_of_probabilities(selected_cards, pair_and_high_card_func),
            "2+2": list_of_probabilities(selected_cards, two_pair_func),
            "3+1": list_of_probabilities(selected_cards, three_of_a_kind_and_high_card_func),
            "3+2": list_of_probabilities(selected_cards, full_house_func)
        },
        "street": {
            "5": list_of_probabilities(selected_cards, street_of_5_func),
            "4": list_of_probabilities(selected_cards, street_of_4_func),
            "3": list_of_probabilities(selected_cards, street_of_3_func),
            "2": list_of_probabilities(selected_cards, street_of_2_func),
            "1": list_of_probabilities(selected_cards, street_of_1_func)
        },
        "flush": {
            "5": list_of_probabilities(selected_cards, flush_of_5_func),
            "4": list_of_probabilities(selected_cards, flush_of_4_func),
            "3": list_of_probabilities(selected_cards, flush_of_3_func),
            "2": list_of_probabilities(selected_cards, flush_of_2_func),
            "1": list_of_probabilities(selected_cards, flush_of_1_func)
        },
        "straight_flush": {
            "5": list_of_probabilities(selected_cards, straight_flush_of_5_func),
            "4": list_of_probabilities(selected_cards, straight_flush_of_4_func),
            "3": list_of_probabilities(selected_cards, straight_flush_of_3_func),
            "2": list_of_probabilities(selected_cards, straight_flush_of_2_func),
            "1": list_of_probabilities(selected_cards, straight_flush_of_1_func)
        }
    }

    with open(OUTPUT_FILE_NAME, "w") as f:
        json.dump(probability_data, f, indent=4)


if __name__ == '__main__':
    main()