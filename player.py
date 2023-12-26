class Player:
    def __init__(self, player_num: int, name: str, chips: int) -> None:
        self._player_num = player_num
        self._name = name
        self._chips = chips
        self._player_cards = []

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
    def player_cards(self):
        return self._player_cards

    @player_cards.setter
    def player_cards(self, value):
        self._player_cards = value

    def fold(self):
        pass

    def call(self):
        pass

    def make_raise(self):
        pass

    def check(self):
        pass


class AIPlayer(Player):
    pass