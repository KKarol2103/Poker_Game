

class Table:
    def __init__(self) -> None:
        self._community_cards = []
        self._stake = 0

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

