# Script generating a JSON file containing the probability of all poker hands in the liar's poker card game
# taking into account cards on your own hand that already match a specified poker hand.

from hand_probability import DeckInfo, HandProbability, CardRequirement
from itertools import repeat
import json

OUTPUT_FILE_NAME: str = "probability_data.json"
DIGITS_OF_PRECISION: int | None = 4
PRETTIFY: bool = False


def list_of_probabilities(func: callable):
    return [func(i) for i in range(1, 24)]


def main():
    deck_info = DeckInfo(deck_size=24, cards_of_rank_count=4, cards_of_suit_count=6)
    hand_probability = HandProbability(deck_info, digits_of_precision=DIGITS_OF_PRECISION)

    probability_data = {
        "highCard": list_of_probabilities(
            hand_probability.create_probability_func(CardRequirement(1, 4))
        ),
        "pair": [
            list_of_probabilities(
                hand_probability.create_probability_func(CardRequirement(2 - matched_cards, 4 - matched_cards))
            )
            for matched_cards in range(2)
        ],
        "threeOfAKind": [
            list_of_probabilities(
                hand_probability.create_probability_func(CardRequirement(3 - matched_cards, 4 - matched_cards))
            )
            for matched_cards in range(3)
        ],
        "fourOfAKind": [
            list_of_probabilities(
                hand_probability.create_probability_func(CardRequirement(4 - matched_cards, 4 - matched_cards))
            )
            for matched_cards in range(4)
        ],
        "twoPair": [[
            list_of_probabilities(
                hand_probability.create_probability_func(
                    CardRequirement(2 - matched_first_cards, 4 - matched_first_cards),
                    CardRequirement(2 - matched_second_cards, 4 - matched_second_cards)
                )
            )
            for matched_second_cards in range(matched_first_cards + 1)
            if matched_second_cards != 2  # case 2+2 is always 100% probable
        ]
            for matched_first_cards in range(3)
        ],
        "fullHouse": [[
            list_of_probabilities(
                hand_probability.create_probability_func(
                    CardRequirement(2 - matched_first_cards, 4 - matched_first_cards),
                    CardRequirement(2 - matched_second_cards, 4 - matched_second_cards)
                )
            )
            for matched_second_cards in range(3)
            if not (matched_first_cards == 3 and matched_second_cards == 2)  # case 3+2 is always 100% probable
        ]
            for matched_first_cards in range(4)
        ],
        "straight": [
            list_of_probabilities(
                hand_probability.at_least_of_ranks_probability_function(*repeat(1, 5 - matched_cards))
            )
            for matched_cards in range(5)
        ],
        "flush": [
            list_of_probabilities(
                hand_probability.create_probability_func(CardRequirement(5 - matched_count, 6 - matched_count))
            )
            for matched_count in range(5)
        ],
        "straightFlush": [
            list_of_probabilities(
                hand_probability.unique_cards_probability_function(5 - matched_count),
            )
            for matched_count in range(5)
        ]
    }

    indent = 4 if PRETTIFY else None
    with open(OUTPUT_FILE_NAME, "w") as f:
        json.dump(probability_data, f, indent=indent)


if __name__ == '__main__':
    main()