from player import Player
from table import Table
import random
from card import Card, Color, Value
from typing import Tuple, List


class Deck:
    def __init__(self) -> None:
        self._cards_in_game: List[Card] = self.init_cards_used_in_a_game()

    @property
    def cards_in_game(self) -> List[Card]:
        return self._cards_in_game

    def init_cards_used_in_a_game(self) -> List[Card]:
        new_deck = []
        for value in Value:
            for color in Color:
                new_deck.append(Card(value, color))
        return new_deck

    def tass_cards(self) -> None:
        # TODO change this method later
        random.shuffle(self._cards_in_game)

    def draw_player_hole_cards(self) -> List[Card]:
        hole_cards = random.sample(self._cards_in_game, 2)
        self._cards_in_game = [card for card in self._cards_in_game if card not in hole_cards]
        return hole_cards

    def take_card_from_deck_and_add_to_com_cards(self, game_table: Table) -> None:
        card = self._cards_in_game.pop(0)
        game_table.community_cards.append(card)

    def put_cards_on_the_table(self, current_round: int, game_table: Table) -> None:
        if current_round < 1 or current_round > 4:
            raise ValueError("Wrong round number")
        if current_round == 2:
            for _ in range(3):
                self.take_card_from_deck_and_add_to_com_cards(game_table)
        if current_round == 3:
            self.take_card_from_deck_and_add_to_com_cards(game_table)
        if current_round == 4:
            self.take_card_from_deck_and_add_to_com_cards(game_table)
