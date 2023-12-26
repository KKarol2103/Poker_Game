class Player:
    def __init__(self, id: int, name: str, money: int) -> None:
        self._id = id
        self._name = name
        self._money = money
        self._player_cards = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = value

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