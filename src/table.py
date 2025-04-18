from typing import List
from card import Card


class Table:
    def __init__(self) -> None:
        self._community_cards: List[Card] = []
        self._stake = 0
        self._current_rate: int = 0

    @property
    def current_rate(self):
        return self._current_rate

    @current_rate.setter
    def current_rate(self, value):
        self._current_rate = value

    @property
    def community_cards(self):
        return self._community_cards

    @community_cards.setter
    def community_cards(self, value):
        self._community_cards = value

    @property
    def stake(self):
        return self._stake

    @stake.setter
    def stake(self, value):
        self._stake = value

    def __str__(self) -> str:
        text = "Cards on the table:"
        text += "\n"
        for card in self._community_cards:
            text += str(card)
            text += " "
        text += "\n"
        text += f'Current Rate: {self._current_rate} Current Stake: {self._stake}'
        return text
