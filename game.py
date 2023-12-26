from player import Player, AIPlayer
from typing import List, Tuple
import random


class Game:
    def __init__(self) -> None:
        self._players_in_game = []
        self._round = 1

    @property
    def players_in_game(self) -> List[Player]:
        return self._players_in_game

    @players_in_game.setter
    def players_in_game(self, value):
        self._players_in_game = value

    @property
    def round(self) -> int:
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

    def get_basic_user_data(self) -> Tuple[str, int]:
        player_name = input("Please enter your name: ")
        player_chips = input("Please enter how many chips you want to have: ")
        return player_name, int(player_chips)

    def draw_the_order_of_players(self) -> None:
        no_all_players_in_game = len(self._players_in_game)
        unique_numbers = random.sample(range(1, no_all_players_in_game + 1), no_all_players_in_game)

        for player, number in zip(self._players_in_game, unique_numbers):
            player.player_num = number

        self._players_in_game.sort(key=lambda player: player.player_num)

    def play(self):
        print("Welcome to the Texas hold'em game!")
        print("Let The Game Begin!")
        player_name, player_chips = self.get_basic_user_data()
        no_opponents = input("How many opponents do you want to have: ")
        self._players_in_game.append(Player(0, player_name, player_chips))

        # TODO to improve later - add external function
        for i in range(int(no_opponents)):
            self._players_in_game.append(AIPlayer(i, f"random{i}", 10000))

        for _ in range(4):
            print(f'Round: {self.get_current_round_name():^30}')
            self._round += 1


def main():
    my_new_game = Game()
    my_new_game.play()


if __name__ == "__main__":
    main()
