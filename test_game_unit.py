from game import Game
from poker_errors import InvalidRoundError
import pytest


def test_get_round_name():
    new_game = Game()
    new_game.round = 3
    assert new_game.get_current_round_name() == "Turn"


def test_incorrect_round_name():
    new_game = Game()
    new_game.round = 6
    with pytest.raises(InvalidRoundError):
        new_game.get_current_round_name()