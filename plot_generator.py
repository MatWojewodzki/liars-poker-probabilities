import matplotlib.pyplot as plt
import numpy as np
from hand_probability import DeckInfo, HandProbability


def main():
    deck_info = DeckInfo(deck_size=24, cards_of_rank_count=4, cards_of_suit_count=6)
    hand_probability = HandProbability(deck_info)

    selected_cards = np.arange(1, deck_info.deck_size)

    high_card_func = hand_probability.at_least_of_ranks_probability_function(1)
    pair_func = hand_probability.at_least_of_ranks_probability_function(2)
    two_pair_func = hand_probability.at_least_of_ranks_probability_function(2, 2)
    straight_func = hand_probability.at_least_of_ranks_probability_function(1, 1, 1, 1, 1)
    three_of_a_kind_func = hand_probability.at_least_of_ranks_probability_function(3)
    full_house_func = hand_probability.at_least_of_ranks_probability_function(3, 2)
    flush_func = hand_probability.at_least_of_suits_probability_function(5)
    four_of_a_kind_func = hand_probability.at_least_of_ranks_probability_function(4)
    straight_flush_func = hand_probability.unique_cards_probability_function(5)

    plt.plot(selected_cards, np.vectorize(high_card_func)(selected_cards), label='High Card')
    plt.plot(selected_cards, np.vectorize(pair_func)(selected_cards), label='Pair')
    plt.plot(selected_cards, np.vectorize(two_pair_func)(selected_cards), label='Two Pair')
    plt.plot(selected_cards, np.vectorize(straight_func)(selected_cards), label='Straight')
    plt.plot(selected_cards, np.vectorize(three_of_a_kind_func)(selected_cards), label='Three of a Kind')
    plt.plot(selected_cards, np.vectorize(full_house_func)(selected_cards), label='Full House')
    plt.plot(selected_cards, np.vectorize(flush_func)(selected_cards), label='Flush')
    plt.plot(selected_cards, np.vectorize(four_of_a_kind_func)(selected_cards), label='Four of a Kind')
    plt.plot(selected_cards, np.vectorize(straight_flush_func)(selected_cards), label='Straight Flush')

    plt.legend()
    plt.title('Probability of a specific poker hand in liar\'s poker (e.g. "a pair of jacks")')
    plt.xlabel("number of cards on the table")
    plt.ylabel("probability")

    plt.show()


if __name__ == '__main__':
    main()