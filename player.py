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

    def compute_player_score(self):
        pass

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
