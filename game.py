from player import Player, AIPlayer
from table import Table
from deck import Deck
from typing import List, Tuple
import random
import time


class Game:
    def __init__(self) -> None:
        self._players_in_game: List[Player] = []
        self._game_deck = Deck()
        self._game_table = Table()
        self._round: int = 1

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

    def get_winner(self) -> Player:
        score_dict = {}
        for player in self._players_in_game:
            player_score = player.compute_player_score(self._game_table)
            score_dict[player.name] = player_score
        return max(score_dict, key=score_dict.get)

    def get_current_player(self) -> Player:
        player = self._players_in_game.pop(0)
        self._players_in_game.append(player)
        return player

    def player_decide_what_to_do(self, player: Player) -> None:
        print("Options:")
        print("1. Fold")
        print("2. Call")
        print("3. Check")
        print("4. Raise")
        choice = int(input("Decide What to do: "))
        if choice == 1:
            player.fold()
        elif choice == 2:
            player.call()
        elif choice == 3:
            player.check()
        elif choice == 4:
            player.make_raise()
        else:
            raise ValueError("Incorrect Choice!")

    def play(self):
        print("Welcome to the Texas hold'em game!")
        print("Let The Game Begin!")
        self._game_deck.tass_cards()
        player_name, player_chips = self.get_basic_user_data()
        no_opponents = input("How many opponents do you want to have: ")
        self._players_in_game.append(Player(0, player_name, player_chips))

        # TODO to improve later - add external function
        for i in range(int(no_opponents)):
            self._players_in_game.append(AIPlayer(i + 1, f"random{i}", 10000))

        self.draw_the_order_of_players()

        for self._round in range(1, 5):
            print(f'Round: {self.get_current_round_name():^30}')
            self._game_deck.put_cards_on_the_table(self._round, self._game_table)
            print(self._game_table)
            print("Now it is time for everyone to decide what to do!")
            print("We will start with: ...")
            for _ in range(len(self._players_in_game)):
                current_player = self.get_current_player()
                print(current_player.name)
                if isinstance(current_player, AIPlayer):
                    print("AI thinks...")
                else:
                    self.player_decide_what_to_do(current_player)
                time.sleep(5)

        print("Time to showdown!")
        winner = self.get_winner()
        print(f'And the winner is: ... {winner} ')



def main():
    my_new_game = Game()
    my_new_game.play()


if __name__ == "__main__":
    main()
