from player import Player
import random
from card import Card, Color, Value
from typing import List


class Deck:
    def __init__(self) -> None:
        self._cards_in_game = []

    @property
    def cards_in_game(self) -> List[Card]:
        return self._cards_in_game

    def init_cards_used_in_a_game(self) -> None:
        for value in Value:
            for color in Color:
                self._cards_in_game.append(Card(value, color))

    def tass_cards(self) -> None:
        random.shuffle(self._cards_in_game)

    def check_player_hand(self, player: Player) -> int:
        pass
