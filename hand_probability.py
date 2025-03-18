from math import comb, prod
from collections.abc import Callable
from itertools import product


class DeckInfo:
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
    def __init__(self, deck_info: DeckInfo):
        self.deck_info = deck_info

    @staticmethod
    def k_from_n_combinations(n: int, k: int) -> int:
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

            return sum(
                prod(
                    (HandProbability.k_from_n_combinations(total_cards_of_a_type, i) for i in card_counts),
                    start=HandProbability.k_from_n_combinations(
                        self.deck_info.deck_size - total_cards_checked, selected_cards_count - sum(card_counts)
                    )
                ) for card_counts in product(*ranges)
            ) / HandProbability.k_from_n_combinations(self.deck_info.deck_size, selected_cards_count)

        return probability_func

    def at_least_of_ranks_probability_function(self, *at_least_of_ranks: int) -> Callable[[int], float]:
        return self._create_probability_func_with_requirements(
            *(CardRankRequirement(count, self.deck_info) for count in at_least_of_ranks))

    def at_least_of_suits_probability_function(self, *at_least_of_suits: int) -> Callable[[int], float]:
        return self._create_probability_func_with_requirements(
            *(CardSuitRequirement(count, self.deck_info) for count in at_least_of_suits))

    def unique_cards_probability_function(self, unique_card_count: int) -> Callable[[int], float]:
        return self._create_probability_func_with_requirements(
            *(UniqueCardRequirement() for _ in range(unique_card_count)))
