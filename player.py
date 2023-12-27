from table import Table
from card import Card, Color, Value
from typing import List, Tuple


class Player:
    def __init__(self, player_num: int = None, name: str = "", chips: int = 0) -> None:
        self._player_num = player_num
        self._name = name
        self._chips = chips
        self._hole_cards = []

    @property
    def player_num(self):
        return self._player_num

    @player_num.setter
    def player_num(self, value):
        self._player_num = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def chips(self):
        return self._chips

    @chips.setter
    def chips(self, value):
        self._chips = value

    @property
    def hole_cards(self):
        return self._hole_cards

    @hole_cards.setter
    def hole_cards(self, value):
        if self._hole_cards:
            raise ValueError
        self._hole_cards = value

    def check_if_there_is_a_straight(self, all_cards: List[Tuple[Color, Value]]) -> bool:
        for i in range(len(all_cards) - 4):
            straight = True
            for j in range(4):
                # TODO refactor it later
                if all_cards[i + j][1].value[0] + 1 != all_cards[i + j + 1][1].value[0]:
                    straight = False
                    break

        return straight

    def compute_player_score(self, game_table: Table) -> int:
        player_and_community_cards = self._hole_cards + game_table.community_cards

        player_points = []
        same_colors = False
        cards_values_dict = {}
        card_colors_dict = {}

        all_cards_values = [(card.color, card.value) for card in player_and_community_cards]
        all_cards_values.sort(key=lambda card_tup: card_tup[1].number)

        is_straight = self.check_if_there_is_a_straight(all_cards_values)
        if is_straight:
            player_points.append(4)

        for color, value in all_cards_values:
            cards_values_dict[value] = cards_values_dict.get(value, 0) + 1
            card_colors_dict[color] = card_colors_dict.get(color, 0) + 1

        most_common_card_value = max(cards_values_dict.values())
        if most_common_card_value == 2:
            player_points.append(1)
        if most_common_card_value == 3:
            player_points.append(3)
        if most_common_card_value == 4:
            player_points.append(7)

        if max(card_colors_dict.values()) == 5:
            same_colors = True
            player_points.append(5)
        if 3 in cards_values_dict.values() and 2 in cards_values_dict.values():
            player_points.append(6)

        if list(cards_values_dict.values()).count(2) == 2:
            player_points.append(2)

        if is_straight and same_colors:
            player_points.append(9)

        if not player_points:
            return 0

        return max(player_points)

    def fold(self):
        pass

    def call(self):
        pass

    def make_raise(self):
        pass

    def check(self):
        pass


class AIPlayer(Player):

    def decide_what_to_do(self):
        pass
