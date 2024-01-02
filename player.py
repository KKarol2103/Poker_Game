from table import Table
from card import Card, Color, Value
from poker_errors import NotEnoughChipsToPlayError, InvalidAmountCheckError
from typing import List, Tuple
import random


class Player:
    def __init__(self, player_num: int = None, name: str = "", chips: int = 0) -> None:
        if player_num < 0:
            raise ValueError("Player num cannot be negative")
        if chips <= 0:
            raise ValueError("Chips number must be positive")
        self._player_num = player_num
        self._name = name
        self._chips = chips
        self._in_game_chips: int = 0
        self._is_active: bool = True
        self._hole_cards: List[Card] = []

    @property
    def player_num(self):
        return self._player_num

    @player_num.setter
    def player_num(self, value):
        if value < 0:
            raise ValueError("Player number cannot be negative")
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
        if value <= 0:
            raise ValueError("Chips number must be positive")
        self._chips = value

    @property
    def hole_cards(self):
        return self._hole_cards

    @hole_cards.setter
    def hole_cards(self, value):
        # if self._hole_cards:
        #     raise ValueError
        self._hole_cards = value

    @property
    def in_game_chips(self):
        return self._in_game_chips

    @in_game_chips.setter
    def in_game_chips(self, value):
        self._in_game_chips = value

    @property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    def check_for_wheel_straight(self, last_card: Card, all_cards: List[Tuple[Color, Value]]) -> bool:
        cards_if_ace_was_on_the_front = all_cards[:4]
        cards_if_ace_was_on_the_front.insert(0, last_card)
        card_numbers = [card[1].value[0] for card in all_cards]
        if all(val in card_numbers for val in [2, 3, 4, 5]):
            return True

    def check_if_there_is_a_straight(self, all_cards: List[Tuple[Color, Value]]) -> bool:
        if len(all_cards) <= 4:
            return False
        for i in range(len(all_cards) - 4):
            straight = True
            for j in range(4):
                # Checking next four cards
                current_card = all_cards[i + j]
                next_card = all_cards[i + j + 1]
                current_card_value = current_card[1].value[0]
                next_card_value = next_card[1].value[0]
                if current_card_value + 1 != next_card_value:
                    straight = False
                    break

        last_card = all_cards[-1]
        last_card_value = last_card[1].value[0]
        if not straight and last_card_value == 14:
            straight = self.check_for_wheel_straight(last_card, all_cards)
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

        if list(cards_values_dict.values()).count(2) >= 2:
            player_points.append(2)

        if is_straight and same_colors:
            values_needded_for_royal_flush = [Value.ACE, Value.KING, Value.QUEEN, Value.JACK, Value.TEN]
            all_royal_values_available = all(val in cards_values_dict.keys() for val in values_needded_for_royal_flush)
            if all_royal_values_available:
                player_points.append(9)
            player_points.append(8)

        if not player_points:
            return 0

        return max(player_points)

    def fold(self) -> None:
        self._is_active = False

    def call(self, game_table: Table) -> None:
        needs_to_put = game_table.current_rate - self._in_game_chips
        if needs_to_put < 0:
            raise NotEnoughChipsToPlayError
        self._in_game_chips += needs_to_put
        self._chips -= needs_to_put

        game_table.stake += needs_to_put

    def make_raise(self, game_table: Table, amount: int) -> None:
        if self._chips - amount < 0:
            raise NotEnoughChipsToPlayError
        self._in_game_chips = game_table.current_rate + amount
        self._chips -= amount

        game_table.current_rate = self._in_game_chips
        game_table.stake += amount

    def check(self, game_table: Table) -> None:
        if game_table.current_rate != self._in_game_chips:
            raise InvalidAmountCheckError

    def show_player_hole_cards(self) -> None:
        cards = ""
        for card in self._hole_cards:
            cards += str(card)
            cards += " "
        print(cards)


class AIPlayer(Player):

    def decide_what_to_do(self, game_table: Table) -> int:
        if self._chips < game_table.current_rate:
            return 1  # FOLD
        hand_strength = self.compute_player_score(game_table)
        cards_on_the_table = len(game_table.community_cards)
        strong_hand = 2  # Good Situation - double pair
        bluff_chance = 0.1
        #  ROUND 1
        first_round = not cards_on_the_table
        if first_round:
            if hand_strength >= 1:
                return 4  # RAISE
            if game_table.current_rate == self._in_game_chips:
                return 3
            return 2

        is_strong = hand_strength >= strong_hand

        if is_strong:
            if game_table.current_rate < self._chips and random.random() < 0.7:
                return 4
            if game_table.current_rate == self._chips and self._in_game_chips == game_table.current_rate:
                return 3
            if game_table.current_rate == self._chips and self._in_game_chips < game_table.current_rate:
                return 2

        if random.random() < bluff_chance:
            return 4  # RAISE (blef)

        if cards_on_the_table == 3 and hand_strength >= 0:
            if game_table.current_rate == self._in_game_chips:
                return 3  # CHECK
            return 2  # CALL

        if cards_on_the_table > 3 and hand_strength == 0:
            return 1  # FOLD

        return 1  # FOLD

    def decide_how_much_to_raise(self, hand_strength: int, game_table: Table) -> int:
        to_raise = 0
        if hand_strength >= 4:
            to_raise = int(game_table.stake * 0.8)
        else:
            to_raise = game_table.stake // 4

        return min(to_raise, self._chips)

    def bluff(self) -> bool:
        pass
