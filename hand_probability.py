from math import comb, prod
from collections.abc import Callable
from itertools import product, repeat


class DeckInfo:
    """
    Represents the information and properties of a playing card deck.

    The DeckInfo class is used to encapsulate essential information about a
    deck of cards, including its size, the count of cards sharing the same rank,
    and the count of cards sharing the same suit.

    :ivar deck_size: Total number of cards in the deck.
    :type deck_size: int
    :ivar cards_of_rank_count: Number of cards for each rank in the deck.
    :type cards_of_rank_count: int
    :ivar cards_of_suit_count: Number of cards for each suit in the deck.
    :type cards_of_suit_count: int
    """
    def __init__(self, deck_size: int, cards_of_rank_count: int, cards_of_suit_count: int):
        self.deck_size = deck_size
        self.cards_of_rank_count = cards_of_rank_count
        self.cards_of_suit_count = cards_of_suit_count


class CardRequirement:
    """
    Represents a requirement that specifies a minimum amount of cards that are present
    among randomly selected cards from a deck.

    :ivar at_least: The minimum number of cards required.
    :type at_least: int
    :ivar out_of: The total number of considered cards present in the deck.
    :type out_of: int

    Example:
        CardRequirement(2, 4) represents a requirement that at least 2 jacks (there are 4 in total) are present
        among randomly selected cards from the deck.
    """
    def __init__(self, at_least: int, out_of: int):
        if at_least < 0 or out_of < 0:
            raise ValueError("at_least and out_of must be positive")
        if at_least > out_of:
            raise ValueError("at_least must be less than or equal to out_of")
        self.at_least = at_least
        self.out_of = out_of


class HandProbability:
    """
    Provides methods for calculating the probability of a given hand in the deck.

    :ivar deck_info: The information related to the deck being utilized.
    :type deck_info: DeckInfo
    :ivar digits_of_precision: The number of decimal places to which probabilities are rounded.
        If None, probabilities are not rounded.
    :type digits_of_precision: int | None
    """
    def __init__(self, deck_info: DeckInfo, digits_of_precision: int | None = None):
        self.deck_info = deck_info
        self.digits_of_precision = digits_of_precision

    @staticmethod
    def _k_from_n_combinations(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return comb(n, k)

    def create_probability_func(self, *card_requirements: CardRequirement) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of a hand described by the specified requirements.
        Cards affected by individual requirements must not overlap.

        :param card_requirements: Requirements for the hand. Each requirement specifies the minimum number
            of cards needed.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of having 3 out of 4 jacks and 2 out of 3 available queens call this function
            as follows:

            func = HandProbability(deck_info).create_probability_func(CardRequirement(3, 4), CardRequirement(2, 3))

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """

        total_cards_checked = 0
        ranges = []
        for card_requirement in card_requirements:
            total_cards_checked += card_requirement.out_of
            ranges.append(range(card_requirement.at_least, card_requirement.out_of + 1))

        def probability_func(selected_cards_count: int) -> float:
            if selected_cards_count < 0:
                raise ValueError("Selected cards count must be non-negative")
            if selected_cards_count > self.deck_info.deck_size:
                raise ValueError("Selected cards count must be less than or equal to deck size")

            probability = sum(
                prod(
                    (HandProbability._k_from_n_combinations(requirement.out_of, count)
                     for requirement, count in zip(card_requirements, card_counts)),
                    start=HandProbability._k_from_n_combinations(self.deck_info.deck_size - total_cards_checked,
                                                                 selected_cards_count - sum(card_counts))
                ) for card_counts in product(*ranges)
            ) / HandProbability._k_from_n_combinations(self.deck_info.deck_size, selected_cards_count)

            return probability if self.digits_of_precision is None else round(probability, self.digits_of_precision)

        return probability_func

    def at_least_of_ranks_probability_function(self, *at_least_of_ranks: int) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of selecting at least the specified number of cards of
        the specified ranks from the deck.

        Wrapper function for create_probability_func() that uses DeckInfo.cards_of_rank_count as the total number
        of cards for every requirement.

        :param at_least_of_ranks: The number of cards of each rank to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting at least 3 kings and at least 2 queens call this function
            as follows:

            func = HandProbability(deck_info).at_least_of_ranks_probability_function(3, 2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self.create_probability_func(
            *(CardRequirement(k, self.deck_info.cards_of_rank_count) for k in at_least_of_ranks)
        )

    def at_least_of_suits_probability_function(self, *at_least_of_suits: int) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of selecting at least the specified number
        of cards of the specified suits from the deck.

        Wrapper function for create_probability_func() that uses DeckInfo.cards_of_suit_count as the total number
        of cards for every requirement.

        :param at_least_of_suits: The number of cards of each suit to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting at least 3 hearts and at least 2 diamonds call this function
            as follows:

            func = HandProbability(deck_info).at_least_of_suits_probability_function(3, 2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self.create_probability_func(
            *(CardRequirement(k, self.deck_info.cards_of_suit_count) for k in at_least_of_suits)
        )

    def unique_cards_probability_function(self, unique_card_count: int) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of selecting the specified number
        of defined unique cards from the deck.

        Wrapper function for create_probability_func() when every card is unique across the deck.

        :param unique_card_count: The number of unique cards to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting ace of spades and king of hearts
            (assuming both cards are unique across the deck) call this function as follows:

            func = HandProbability(deck_info).unique_cards_probability_function(2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self.create_probability_func(
            *repeat(CardRequirement(1, 1), unique_card_count)
        )
