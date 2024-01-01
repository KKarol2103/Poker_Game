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

    def create_opponents(self) -> None:
        no_opponents = int(input("How many opponents do you want to have: "))
        opponents_chips = int(input("How many chips shouuld opponents have: "))
        for i in range(no_opponents):
            self._players_in_game.append(AIPlayer(i + 1, f"random{i}", opponents_chips))

    def draw_the_order_of_players(self) -> None:
        no_all_players_in_game = len(self._players_in_game)
        unique_numbers = random.sample(range(1, no_all_players_in_game + 1), no_all_players_in_game)

        for player, number in zip(self._players_in_game, unique_numbers):
            player.player_num = number

        self._players_in_game.sort(key=lambda player: player.player_num)

    def get_winner(self) -> Tuple[Player, int]:
        score_dict = {}
        for player in self._players_in_game:
            if player.is_active:
                player_score = player.compute_player_score(self._game_table)
                score_dict[player] = player_score
        player_with_max_score = max(score_dict, key=score_dict.get)
        return player_with_max_score, score_dict[player_with_max_score]

    def get_current_player(self) -> Player:
        player = self._players_in_game.pop(0)
        self._players_in_game.append(player)
        return player

    def player_decide_what_to_do(self, player: Player) -> int:
        if isinstance(player, AIPlayer):
            choice = player.decide_what_to_do(self._game_table)
        else:
            print("Options:")
            print("1. Fold")
            print("2. Call")
            print("3. Check")
            print("4. Raise")
            choice = int(input("Decide What to do: "))
        if choice == 1:
            print("Player Folds")
            player.fold()
        elif choice == 2:
            print("Player Calls")
            player.call(self._game_table)
        elif choice == 3:
            print("Player Checks")
            player.check(self._game_table)
        elif choice == 4:
            if isinstance(player, AIPlayer):
                amount = player.decide_how_much_to_raise(self._game_table)
            else:
                amount = int(input("Raise Amount: "))
            print(f"Player Raises by {amount}")
            player.make_raise(self._game_table, amount)
        else:
            raise ValueError("Incorrect Choice!")

        return choice

    def deal_the_cards(self) -> None:
        for player in self._players_in_game:
            player.hole_cards = self._game_deck.draw_player_hole_cards()

    def mark_all_players_as_active(self) -> None:
        for player in self._players_in_game:
            player.is_active = True

    def check_all_players_matched(self) -> bool:
        return all(player.in_game_chips == self._game_table.current_rate or not player.is_active for player in self._players_in_game)

    def check_only_one_player_left(self) -> bool:
        return sum(player.is_active for player in self._players_in_game) == 1

    def assign_bets_to_big_blind_and_small_blind(self) -> Tuple[str, str]:
        dealer = self._players_in_game[0]
        small_blind_player = self._players_in_game[1]
        big_blind_player = self._players_in_game[2]
        small_blind_player.make_raise(self._game_table, 10)
        big_blind_player.make_raise(self._game_table, 20)
        dealer.name += " D "
        small_blind_player.name += " SB "
        big_blind_player.name += " BB "

        return (small_blind_player.name, big_blind_player.name)

    def conduct_betting_round(self) -> None:
        if self._round == 1:
            small_blind, big_blind = self.assign_bets_to_big_blind_and_small_blind()
            print(f"Small Blind Player - {small_blind} Raises by: 10")
            print(f"Big Blind Player - {big_blind} Raises by: 20")
            time.sleep(3)
        raise_made = True
        last_raiser = None
        dealer_played = False
        while (raise_made):
            raise_made = False
            for index, player in enumerate(self._players_in_game):
                current_player = self.get_current_player()
                print(30 * "-")
                print(current_player.name)
                if self._round == 1 and index < 3 and not dealer_played:
                    continue

                if current_player.is_active:
                    if isinstance(current_player, AIPlayer):
                        print("AI thinks...")
                    else:
                        print(30 * "-")
                        print(self._game_table)
                        print("Your Cards: ")
                        current_player.show_player_hole_cards()
                        print(f"Your in game chips: {current_player.in_game_chips}")

                    choice = self.player_decide_what_to_do(current_player)
                    print(30 * "-")

                    if choice == 4:
                        last_raiser = current_player
                        raise_made = True
                    elif last_raiser == current_player:
                        raise_made = False
                        break

                    time.sleep(3)

            if self._round == 1 and not dealer_played:
                dealer_played = True
                dealer = self._players_in_game[0]
                print(30 * "-")
                print(dealer.name)
                choice = self.player_decide_what_to_do(dealer)
                print(30 * "-")

                if choice == 4:
                    raise_made = True

                time.sleep(3)

            if self.check_only_one_player_left():
                break

            if not raise_made and self.check_all_players_matched():
                break

            time.sleep(3)

    def play(self):
        running = True
        print("Welcome to the Texas hold'em game!")
        print("Let The Game Begin!")
        player_name, player_chips = self.get_basic_user_data()
        new_player = Player(0, player_name, player_chips)
        self._players_in_game.append(new_player)
        self.create_opponents()
        while (running):
            self.mark_all_players_as_active()
            self._game_deck.shuffle_cards()
            self.draw_the_order_of_players()
            self.deal_the_cards()
            print("Your Cards: ")
            new_player.show_player_hole_cards()

            for self._round in range(1, 5):
                print(f'Round: {self.get_current_round_name()}')
                only_one_left = self.check_only_one_player_left()
                if only_one_left:
                    print("Only One Player Left")
                    break
                print(30 * "-")
                time.sleep(3)
                self._game_deck.put_cards_on_the_table(self._round, self._game_table)
                print(self._game_table)
                print("Now it is time for everyone to decide what to do!")
                print(30 * "-")
                time.sleep(3)
                print("Current Player: ")
                time.sleep(1)
                self.conduct_betting_round()

            print("Time to showdown!")
            time.sleep(2)
            winner, score = self.get_winner()
            print('And the winner is: ...')
            time.sleep(3)
            print(f"{winner.name} ! with result {score}'")
            print("His Cards Were: ")
            time.sleep(1)
            winner.show_player_hole_cards()
            winner.chips += self._game_table.stake
            print(f"Your current chips status: {new_player.chips}")
            decision = input("Would You Like to Play Again? [Y/N]: ")
            if decision == "N":
                running = False
            print(" ")
        print("See You Soon!")


def main():
    my_new_game = Game()
    my_new_game.play()


if __name__ == "__main__":
    main()
