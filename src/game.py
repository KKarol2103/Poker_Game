from player import Player, AIPlayer
from table import Table
from deck import Deck
from poker_errors import (SinglePlayerWantsToFoldError, InvalidActionError,
                          NotEnoughChipsToPlayError, InvalidAmountCheckError,
                          InvalidInputData, InvalidRoundError)
from typing import List, Tuple
import random
import time


class Game:
    def __init__(self) -> None:
        self._players_in_game: List[Player] = []
        self._game_deck = Deck()
        self._game_table = Table()

    @property
    def players_in_game(self) -> List[Player]:
        return self._players_in_game

    @players_in_game.setter
    def players_in_game(self, value):
        self._players_in_game = value

    def get_round_name(self, current_round: int) -> str:
        if current_round == 1:
            return "Pre-Flop"
        if current_round == 2:
            return "Flop"
        if current_round == 3:
            return "Turn"
        if current_round == 4:
            return "River"
        raise InvalidRoundError

    def get_basic_user_data(self) -> Tuple[str, int]:
        player_name = input("Please enter your name: ")
        player_chips = input("Please enter how many chips you want to have: ")
        return player_name, int(player_chips)

    def create_opponents(self, player_chips: int) -> None:
        no_opponents = int(input("How many opponents do you want to have: "))
        opponents_chips = player_chips
        if no_opponents <= 0 or opponents_chips < 30:
            raise InvalidInputData
        for i in range(no_opponents):
            self._players_in_game.append(AIPlayer(f"random{i}", opponents_chips))

    def draw_the_order_of_players(self) -> None:
        no_all_players_in_game = len(self._players_in_game)
        unique_numbers = random.sample(range(1, no_all_players_in_game + 1), no_all_players_in_game)

        for player, number in zip(self._players_in_game, unique_numbers):
            player.player_num = number

        self._players_in_game.sort(key=lambda player: player.player_num)

    def get_winner(self) -> Tuple[List[Player], int]:
        score_dict = {}
        for player in self._players_in_game:
            if player.is_active:
                player_score = player.compute_player_score(self._game_table)
                score_dict[player] = player_score
        max_score = max(score_dict.values())
        winners = [player for player, score in score_dict.items() if score == max_score]
        return winners, max_score

    def get_player_and_move_to_served(self, un_served_players: List[Player], served_players: List[Player]) -> Player:
        current_player = un_served_players.pop(0)
        served_players.append(current_player)
        return current_player

    def player_decide_what_to_do(self, player: Player, no_raises: int) -> int:
        if isinstance(player, AIPlayer):
            choice = player.decide_what_to_do(self._game_table, no_raises)
        else:
            print("Options:")
            print("1. Fold")
            print("2. Call")
            print("3. Check")
            print("4. Raise")
            to_call_amount = self._game_table.current_rate - player.in_game_chips
            print(f"To Call You have to put at least {to_call_amount}")
            choice = int(input("Decide What to do: "))
        if choice == 1:
            if self.check_one_player_left() == 1:
                raise SinglePlayerWantsToFoldError
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
                hand_strength = player.compute_player_score(self._game_table)
                amount = player.decide_how_much_to_raise(hand_strength, self._game_table)
            else:
                amount = int(input("Raise Amount: "))
            print(f"Player Raises by {amount}")
            player.make_raise(self._game_table, amount)
        else:
            raise InvalidActionError

        return choice

    def deal_the_cards(self) -> None:
        for player in self._players_in_game:
            player.hole_cards = self._game_deck.draw_player_hole_cards()

    def split_prize(self, winners_of_game: List[Player], reward: int) -> None:
        no_winners = len(winners_of_game)
        reward_for_single_player = reward // no_winners
        for player in winners_of_game:
            player.chips += reward_for_single_player

    def reset_players(self) -> None:
        for index, player in enumerate(self._players_in_game):
            player.is_active = True
            player.in_game_chips = 0
            if index < 3:
                player.name = player.name[:-3]

    def check_all_players_matched(self) -> bool:
        return all(player.in_game_chips == self._game_table.current_rate or not player.is_active
                   for player in self._players_in_game)

    def check_one_player_left(self) -> bool:
        return sum(player.is_active for player in self._players_in_game) == 1

    def assign_blinds_bets(self) -> Tuple[Player, Player]:
        dealer = self._players_in_game[0]
        small_blind_player = self._players_in_game[1]
        big_blind_player = self._players_in_game[2]
        small_blind_player.make_raise(self._game_table, 1)
        big_blind_player.make_raise(self._game_table, 1)
        dealer.name += " D "
        small_blind_player.name += " SB "
        big_blind_player.name += " BB "

        return small_blind_player, big_blind_player

    def get_player_decision(self, player: Player, no_raises: int) -> int:
        decided = False
        while (not decided):
            try:
                choice = self.player_decide_what_to_do(player, no_raises)
            except (InvalidActionError, ValueError):
                print("\nInvalid Option! Try Again\n")
                continue
            except InvalidAmountCheckError:
                print("To check your in_game chips must be equal to current rate!")
                print("Try Again")
                continue
            except NotEnoughChipsToPlayError:
                print("You don't have enough chips to do that!")
                print("Choose other Action")
                continue
            except SinglePlayerWantsToFoldError:
                print("It is not possible for one player to fold")
                choice = 2
                break
            decided = True
        return choice

    def conduct_betting_round(self, current_round: int) -> None:
        last_raiser = None
        if current_round == 1:
            small_blind, big_blind = self.assign_blinds_bets()
            print(f"Small Blind Player - {small_blind.name} sets small blind value to: 1")
            print(f"Big Blind Player - {big_blind.name} sets big blind value to: 2")
            last_raiser = big_blind
            time.sleep(3)

        raise_made = True
        encirlcment = 0
        no_raises = 0
        un_served_players = self._players_in_game[:]
        served_players = []
        while (raise_made):
            raise_made = False
            while un_served_players:
                current_player = self.get_player_and_move_to_served(un_served_players, served_players)
                print(30 * "-")
                if current_round == 1 and current_player.player_num < 4 and not encirlcment:
                    #  During First Round and first encirlcment
                    #  small and big blind players have already bet
                    print(current_player.name)
                    time.sleep(3)
                    raise_made = True
                    continue

                if current_player.is_active:
                    if not isinstance(current_player, AIPlayer):
                        print("It's Your Turn!")
                        print(self._game_table)

                    print(current_player)

                    choice = self.get_player_decision(current_player, no_raises)

                    if choice == 4:
                        last_raiser = current_player
                        no_raises += 1
                        raise_made = True
                    elif last_raiser == current_player:
                        raise_made = False
                        break
                    time.sleep(3)

                else:
                    print(f"{current_player} - NOT ACTIVE")

            encirlcment += 1
            un_served_players, served_players = served_players, un_served_players
            served_players.clear()

            if self.check_one_player_left():
                break

            if not raise_made and self.check_all_players_matched():
                break

    def play(self):
        running = True
        print("Welcome to the Texas hold'em game!")
        print("Let The Game Begin!")
        try:
            player_name, player_chips = self.get_basic_user_data()
            new_player = Player(player_name, player_chips)
            self._players_in_game.append(new_player)
            self.create_opponents(player_chips)
        except ValueError:
            print("Invalid Data given")
            return
        except InvalidInputData:
            print("Invalid Oponnents Data given")
            return
        while (running):
            self._game_deck.shuffle_cards()
            self.draw_the_order_of_players()
            self.deal_the_cards()
            print("Your Cards: ")
            print(new_player.player_hole_cards_desc())
            round = 0

            for round in range(1, 5):
                print(f'Round: {self.get_round_name(round)}')
                only_one_left = self.check_one_player_left()
                if only_one_left:
                    print("Only One Player Left")
                    break
                print(30 * "-")
                time.sleep(3)
                self._game_deck.put_cards_on_the_table(round, self._game_table)
                print(self._game_table)
                print("Now it is time for everyone to decide what to do!")
                print(30 * "-")
                time.sleep(3)
                print("Current Player: ")
                time.sleep(1)
                self.conduct_betting_round(round)

            print("Time to showdown!")
            time.sleep(2)
            winners, score = self.get_winner()
            if len(winners) == 1:
                winner = winners[0]
                print('And the winner is: ...')
                time.sleep(3)
                print(winner)
                print(f"With score: {score}")
                winner.chips += self._game_table.stake
            else:
                print("Draw! There is more than one winner!")
                print("The Winners are: ")
                for winner in winners:
                    print(winner)
                self.split_prize(winners, self._game_table.stake)
            print(f"Your chips after game : {new_player.chips}")
            decision = input("Would You Like to Play Again? [Y/N]: ")
            if decision == "N":
                running = False
            else:
                self._game_deck = Deck()
                self._game_table = Table()
                self.reset_players()
            print(" ")
        print("See You Soon!")
