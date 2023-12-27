from table import Table


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

    def compute_player_score(self, game_table: Table) -> int:
        player_and_community_cards = self._hole_cards + game_table.community_cards
        cards_values_dict = {}
        card_colors_dict = {}
        all_cards_values_dict = [(card.color, card.value) for card in player_and_community_cards]
        player_points = []
        for color, value in all_cards_values_dict:
            cards_values_dict[value] = cards_values_dict.get(value, 0) + 1
            card_colors_dict[color] = card_colors_dict.get(color, 0) + 1

        if max(cards_values_dict.values()) == 2:
            player_points.append(1)
        if max(cards_values_dict.values()) == 3:
            player_points.append(3)
        if max(cards_values_dict.values()) == 4:
            player_points.append(4)

        if max(card_colors_dict.values()) == 5:
            player_points.append(5)
        if 3 in cards_values_dict.values() and 2 in cards_values_dict.values():
            player_points.append(6)

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
