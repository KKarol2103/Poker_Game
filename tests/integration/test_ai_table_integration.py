from card import Card, Color, Value
from table import Table
from player import AIPlayer
import pytest


@pytest.fixture(autouse=True)
def mock_random(monkeypatch):
    monkeypatch.setattr('random.random', lambda: 0.3)


def test_aiplayer_raise():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.KING, Color.CLUBS), Card(Value.KING, Color.DIAMONDS), Card(Value.KING, Color.CLUBS)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table, 0) == 4


def test_aiplayer_how_much_to_raise_very_strong_hand():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    game_table.current_rate = 100
    game_table.stake = 250
    ai_player._in_game_chips = 100
    assert ai_player.decide_how_much_to_raise(4, game_table) == 83


def test_aiplayer_how_much_to_raise_stake_bigger_than_chips():
    ai_player = AIPlayer(name="AIPlayer", chips=50)
    game_table = Table()
    game_table.current_rate = 100
    game_table.stake = 250
    ai_player._in_game_chips = 25
    assert ai_player.decide_how_much_to_raise(4, game_table) == 1


def test_aiplayer_how_much_to_raise_medium_hand():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    game_table.current_rate = 100
    game_table.stake = 250
    ai_player._in_game_chips = 100
    assert ai_player.decide_how_much_to_raise(2, game_table) == 62


def test_aiplayer_raise_first_round():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    ai_player.hole_cards = [Card(Value.TWO, Color.CLUBS), Card(Value.TWO, Color.DIAMONDS)]
    assert ai_player.decide_what_to_do(game_table, 0) == 4


def test_aiplayer_would_raise_but_frequent_raises_before():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    ai_player.hole_cards = [Card(Value.TWO, Color.CLUBS), Card(Value.TWO, Color.DIAMONDS)]
    assert ai_player.decide_what_to_do(game_table, 4) == 3


def test_aiplayer_call():
    ai_player = AIPlayer(name="AIPlayer", chips=100)
    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.KING, Color.CLUBS), Card(Value.KING, Color.DIAMONDS), Card(Value.KING, Color.CLUBS)]
    ai_player._in_game_chips = 0
    assert ai_player.decide_what_to_do(game_table, 0) == 2


def test_aiplayer_check():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)

    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.TWO, Color.DIAMONDS), Card(Value.FIVE, Color.CLUBS), Card(Value.ACE, Color.SPADES)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table, 0) == 3


def test_aiplayer_check_strong_hand_equal_chips_to_current_rate():
    ai_player = AIPlayer(name="AIPlayer", chips=0)

    game_table = Table()
    ai_player.hole_cards = [Card(Value.ACE, Color.DIAMONDS), Card(Value.TEN, Color.HEARTS)]
    ai_player._in_game_chips = 1000
    game_table.current_rate = 1000
    game_table.community_cards = [Card(Value.TWO, Color.DIAMONDS), Card(Value.TWO, Color.CLUBS), Card(Value.ACE, Color.SPADES)]
    assert ai_player.decide_what_to_do(game_table, 0) == 3


def test_aiplayer_fold():
    ai_player = AIPlayer(name="AIPlayer", chips=100)

    game_table = Table()
    game_table.community_cards = [Card(Value.NINE, Color.HEARTS), Card(Value.SEVEN, Color.DIAMONDS)]
    game_table.current_rate = 300
    game_table.community_cards = [Card(Value.TWO, Color.DIAMONDS), Card(Value.FIVE, Color.CLUBS), Card(Value.ACE, Color.SPADES), Card(Value.JACK, Color.SPADES)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table, 0) == 1


def test_ai_player_not_enough_chips_to_play():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 2000
    assert ai_player.decide_what_to_do(game_table, 0) == 1


def test_ai_player_how_much_to_raise():
    ai_player = AIPlayer(name="AIPlayer", chips=1000)
    game_table = Table()
    ai_player.in_game_chips = 100
    game_table.current_rate = 250
    game_table.stake = 400
    how_much = ai_player.decide_how_much_to_raise(4, game_table)
    assert how_much == 133
