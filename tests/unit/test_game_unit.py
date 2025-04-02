from game import Game
from poker_errors import InvalidRoundError
import pytest


def test_get_round_name():
    new_game = Game()
    assert new_game.get_round_name(3) == "Turn"


def test_incorrect_round_name():
    new_game = Game()
    with pytest.raises(InvalidRoundError):
        new_game.get_round_name(6)
