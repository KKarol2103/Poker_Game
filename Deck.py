from player import Player
from Card import Card, Color, Value
from typing import List


class Deck:
    def __init__(self) -> None:
        self._cards_in_game = []

    @property
    def cards_in_game(self) -> List[Card]:
        return self._cards_in_game

    def init_cards_used_in_a_game(self):
        for value in Value:
            for color in Color:
                self._cards_in_game.append(Card(value.name, color.name))

    def tass_cards(self):
        pass

    def check_player_hand(self, player: Player) -> int:
        pass
