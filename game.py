from player import Player, AIPlayer


class Game:
    def __init__(self) -> None:
        self._players_in_game = []
        self._round = 1

    @property
    def players_in_game(self):
        return self._players_in_game

    @players_in_game.setter
    def players_in_game(self, value):
        self._players_in_game = value

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, value):
        self._round = value

    def get_current_round_name(self) -> str:
        if self._round == 1:
            return "Pre-Flop"
        if self._round == 2:
            return "Flop"
        if self._round == 3:
            return "Turn"
        if self._round == 4:
            return "River"
        raise ValueError("Incorrect round number")

    def play(self):
        print("Let The Game Begin!")
        print()
        no_opponents = input("How many opponents do you want to have: ")
        for i in range(int(no_opponents)):
            self._players_in_game.append(AIPlayer(i, f"random{i}", 10000))  # TODO to improve later
        while (True):
            print(f'Round: {self.get_current_round_name():^30}')


def main():
    my_new_game = Game()
    my_new_game.play()


if __name__ == "__main__":
    main()
