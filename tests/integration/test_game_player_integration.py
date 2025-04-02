from player import Player, AIPlayer
from game import Game
from poker_errors import InvalidAmountCheckError
import random
import pytest


def mock_random_sample(range, k):
    return [4, 1, 3, 2]


def test_draw_the_order_of_players(monkeypatch):
    new_game = Game()
    new_game.players_in_game = [Player(), AIPlayer(), AIPlayer(), AIPlayer()]
    monkeypatch.setattr(random, "sample", mock_random_sample)
    new_game.draw_the_order_of_players()

    expected_order = [1, 2, 3, 4]
    actual_order = [player.player_num for player in new_game.players_in_game]
    assert actual_order == expected_order


def mock_compute_player_score(self, table):
    if isinstance(self, AIPlayer):
        return 4
    else:
        return 6


def test_get_winner(monkeypatch):
    game = Game()
    monkeypatch.setattr(Player, "compute_player_score", mock_compute_player_score)
    monkeypatch.setattr(AIPlayer, "compute_player_score", mock_compute_player_score)
    normal_player = Player("Gracz")
    first_ai_player = AIPlayer()
    second_ai_player = AIPlayer()
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]
    winner, score = game.get_winner()
    assert len(winner) == 1
    assert winner[0].name == "Gracz"
    assert score == 6


def mock_same_results(self, table):
    return 4


def test_get_winner_more_than_one_player(monkeypatch):
    game = Game()
    monkeypatch.setattr(Player, "compute_player_score", mock_same_results)
    monkeypatch.setattr(AIPlayer, "compute_player_score", mock_same_results)
    normal_player = Player("Gracz")
    first_ai_player = AIPlayer()
    second_ai_player = AIPlayer()
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]
    winners, score = game.get_winner()
    assert len(winners) == 3
    assert winners[0].name == "Gracz"
    assert score == 4


def test_split_prize():
    game = Game()
    normal_player = Player("Gracz")
    first_ai_player = AIPlayer()
    second_ai_player = AIPlayer()
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]
    game.split_prize(game.players_in_game, 3000)
    for player in game.players_in_game:
        assert player.chips == 1000


def test_split_prize2():
    game = Game()
    normal_player = Player("Gracz")
    normal_player.chips = 1200
    first_ai_player = AIPlayer()
    second_ai_player = AIPlayer()
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]
    game.split_prize(game.players_in_game, 3000)
    assert normal_player.chips == 2200


def test_get_current_player():
    game = Game()
    normal_player = Player("Gracz")
    first_ai_player = AIPlayer()
    second_ai_player = AIPlayer()
    unserved_players = [normal_player, first_ai_player, second_ai_player]
    served_players = []

    game.get_player_and_move_to_served(unserved_players, served_players)
    assert unserved_players == [first_ai_player, second_ai_player]
    assert served_players == [normal_player]


def test_player_call():
    game = Game()
    normal_player = Player("Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 700
    normal_player._chips = 500
    normal_player._in_game_chips = 100

    normal_player.call(game._game_table)
    assert normal_player.chips == 200
    assert normal_player.in_game_chips == 400


def test_player_check():
    game = Game()
    normal_player = Player("Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 1400
    normal_player._chips = 500
    normal_player._in_game_chips = 400
    normal_player.check(game._game_table)  # No Err


def test_attempt_to_check_when_rate_is_bigger_than_player_chips():
    game = Game()
    normal_player = Player("Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 1400
    normal_player._chips = 500
    normal_player._in_game_chips = 200
    with pytest.raises(InvalidAmountCheckError):
        normal_player.check(game._game_table)


def test_player_make_raise():
    game = Game()
    normal_player = Player("Gracz")
    game._game_table.current_rate = 200
    game._game_table.stake = 300
    normal_player._chips = 500
    normal_player._in_game_chips = 200
    normal_player.make_raise(game._game_table, 200)
    assert game._game_table.current_rate == 400
    assert game._game_table.stake == 500
    assert normal_player._chips == 300
    assert normal_player._in_game_chips == 400


def test_check_if_all_players_matched():
    game = Game()
    player = Player(chips=1000)
    first_ai_player = AIPlayer(1, chips=500)
    second_ai_player = AIPlayer(2, chips=500)
    game.players_in_game = [player, first_ai_player, second_ai_player]
    game._game_table.current_rate = 200
    player.in_game_chips = 200
    first_ai_player.in_game_chips = 200
    second_ai_player.is_active = False
    assert game.check_all_players_matched() is True
