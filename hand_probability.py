from math import comb, prod
from collections.abc import Callable
from itertools import product


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


class CardCountRequirement:
    def __init__(self, required_count: int, total_count: int):
        self.required_count = required_count
        self.total_count = total_count

    def __repr__(self):
        return f"{self.__class__.__name__}(required_count={self.required_count}, total_count={self.total_count})"


class CardRankRequirement(CardCountRequirement):
    def __init__(self, required_count: int, deck_info: DeckInfo):
        super().__init__(required_count, deck_info.cards_of_rank_count)


class CardSuitRequirement(CardCountRequirement):
    def __init__(self, required_count: int, deck_info: DeckInfo):
        super().__init__(required_count, deck_info.cards_of_suit_count)


class UniqueCardRequirement(CardCountRequirement):
    def __init__(self):
        super().__init__(1, 1)


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

    @staticmethod
    def _check_requirement_integrity(*requirements: CardCountRequirement) -> None:
        if all(isinstance(requirement, CardRankRequirement) for requirement in requirements):
            return
        if all(isinstance(requirement, CardSuitRequirement) for requirement in requirements):
            return
        if all(isinstance(requirement, UniqueCardRequirement) for requirement in requirements):
            return

        raise TypeError("All requirements must be either of type CardRankRequirement, CardSuitRequirement or UniqueCardRequirement")

    def _create_probability_func_with_requirements(self, *requirements: CardCountRequirement) -> Callable[[int], float]:
        HandProbability._check_requirement_integrity(*requirements)

        total_cards_of_a_type = requirements[0].total_count

        ranges = []
        total_cards_checked = 0
        for requirement in requirements:
            ranges.append(range(requirement.required_count, requirement.total_count + 1))
            total_cards_checked += requirement.total_count

        def probability_func(selected_cards_count: int) -> float:
            if selected_cards_count < 0:
                raise ValueError("Selected cards count must be non-negative")
            if selected_cards_count > self.deck_info.deck_size:
                raise ValueError("Selected cards count must be less than or equal to deck size")

            probability = sum(
                prod(
                    (HandProbability._k_from_n_combinations(total_cards_of_a_type, i) for i in card_counts),
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

        :param at_least_of_ranks: The number of cards of each rank to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting at least 3 kings and at least 2 queens call this function
            as follows:

            func = HandProbability(deck_info).at_least_of_ranks_probability_function(3, 2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self._create_probability_func_with_requirements(
            *(CardRankRequirement(count, self.deck_info) for count in at_least_of_ranks))

    def at_least_of_suits_probability_function(self, *at_least_of_suits: int) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of selecting at least the specified number
        of cards of the specified suits from the deck.

        :param at_least_of_suits: The number of cards of each suit to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting at least 3 hearts and at least 2 diamonds call this function
            as follows:

            func = HandProbability(deck_info).at_least_of_suits_probability_function(3, 2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self._create_probability_func_with_requirements(
            *(CardSuitRequirement(count, self.deck_info) for count in at_least_of_suits))

    def unique_cards_probability_function(self, unique_card_count: int) -> Callable[[int], float]:
        """
        Returns a function that calculates the probability of selecting the specified number
        of defined unique cards from the deck.

        :param unique_card_count: The number of unique cards to be selected.
        :return: A function that calculates the probability of having the hand based on the number
            of selected cards.

        Example:
            To calculate the probability of selecting ace of spades and king of hearts
            (assuming both cards are unique across the deck) call this function as follows:

            func = HandProbability(deck_info).unique_cards_probability_function(2)

            func(12) returns the probability of the hand when 12 random cards are selected from the deck
        """
        return self._create_probability_func_with_requirements(
            *(UniqueCardRequirement() for _ in range(unique_card_count)))
