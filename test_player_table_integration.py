from card import Card, Color, Value
from table import Table
from player import Player
from poker_errors import NotEnoughChipsToPlayError
import pytest


def test_compute_player_score_high_card():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.EIGHT, Color.HEARTS)]
    game_table.community_cards = [Card(Value.NINE, Color.HEARTS),
                                  Card(Value.KING, Color.DIAMONDS),
                                  Card(Value.TWO, Color.SPADES),
                                  Card(Value.ACE, Color.HEARTS),
                                  Card(Value.TEN, Color.CLUBS)]
    player.compute_player_score(game_table) == 0


def test_compute_player_score_pair():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.QUEEN, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.KING, Color.DIAMONDS),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    player.compute_player_score(game_table) == 1


def test_compute_player_score_double_pair():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.QUEEN, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.QUEEN, Color.DIAMONDS),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 2


def test_compute_player_score_three_of_a_kind():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.SEVEN, Color.CLUBS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.KING, Color.DIAMONDS),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 3


def test_compute_player_score_straight():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.FIVE, Color.HEARTS), Card(Value.SIX, Color.CLUBS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.DIAMONDS),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.NINE, Color.HEARTS),
                                  Card(Value.TWO, Color.CLUBS),
                                  Card(Value.THREE, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 4


def test_compute_player_score_broadway_straight():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.ACE, Color.HEARTS), Card(Value.KING, Color.SPADES)]
    game_table.community_cards = [Card(Value.QUEEN, Color.DIAMONDS),
                                  Card(Value.JACK, Color.CLUBS),
                                  Card(Value.TEN, Color.HEARTS),
                                  Card(Value.THREE, Color.SPADES),
                                  Card(Value.TWO, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 4


def test_compute_player_score_wheel_straight():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.ACE, Color.HEARTS), Card(Value.TWO, Color.SPADES)]
    game_table.community_cards = [Card(Value.THREE, Color.DIAMONDS),
                                  Card(Value.FOUR, Color.CLUBS),
                                  Card(Value.FIVE, Color.HEARTS),
                                  Card(Value.SEVEN, Color.SPADES),
                                  Card(Value.EIGHT, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 4


def test_compute_player_score_flush():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.TWO, Color.HEARTS), Card(Value.FIVE, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.KING, Color.HEARTS),
                                  Card(Value.EIGHT, Color.HEARTS),
                                  Card(Value.JACK, Color.DIAMONDS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 5


def test_compute_player_score_full_house():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.SEVEN, Color.HEARTS)]
    game_table.community_cards = [Card(Value.KING, Color.CLUBS),
                                  Card(Value.KING, Color.SPADES),
                                  Card(Value.KING, Color.DIAMONDS),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 6


def test_compute_player_score_four_of_a_kind():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.SEVEN, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.CLUBS),
                                  Card(Value.SEVEN, Color.SPADES),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 7


def test_compute_player_score_straight_flush():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.NINE, Color.HEARTS), Card(Value.EIGHT, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.SIX, Color.HEARTS),
                                  Card(Value.FIVE, Color.HEARTS),
                                  Card(Value.THREE, Color.SPADES),
                                  Card(Value.TWO, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 8


def test_compute_player_score_royal_flush():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.ACE, Color.HEARTS), Card(Value.KING, Color.HEARTS)]
    game_table.community_cards = [Card(Value.QUEEN, Color.HEARTS),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.TEN, Color.HEARTS),
                                  Card(Value.THREE, Color.SPADES),
                                  Card(Value.TWO, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 9


def test_compute_player_score_three_pairs():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.TWO, Color.HEARTS), Card(Value.EIGHT, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.SEVEN, Color.CLUBS),
                                  Card(Value.FIVE, Color.HEARTS),
                                  Card(Value.FIVE, Color.SPADES),
                                  Card(Value.TWO, Color.DIAMONDS)]
    assert player.compute_player_score(game_table) == 2


def test_player_makes_raise_2():
    player = Player(chips=1000)
    table = Table()
    player.in_game_chips = 250
    table.current_rate = 300
    table.stake = 600
    raise_amount = 300

    player.make_raise(table, raise_amount)

    assert table.current_rate == 600
    assert table.stake == 600 + 350

    assert player._chips == 1000 - 350
    assert player._in_game_chips == 250 + 50 + 300


def test_player_make_raise_3():
    player = Player(chips=500)
    table = Table()
    table.current_rate = 50
    table.stake = 100
    player._in_game_chips = 25

    player.make_raise(table, 75)

    assert table.current_rate == 125
    assert table.stake == 200
    assert player._chips == 400
    assert player._in_game_chips == 125


def test_player_make_raise_4():
    player = Player(chips=420)
    table = Table()
    table.current_rate = 379 + 123
    table.stake = 1339
    player._in_game_chips = 30

    with pytest.raises(NotEnoughChipsToPlayError):
        player.make_raise(table, 334)

    # assert table.current_rate == 125
    # assert table.stake == 200
    # assert player._chips == 400
    # assert player._in_game_chips == 125


# def test_player_makes_raise_but_ammount_is_too_low():
#     player = Player(chips=348)
#     table = Table()
#     player.in_game_chips = 102
#     raise_amount = 1
#     table.current_rate = 331
#     table.stake = 2521

#     with pytest.raises(TooLowRaiseError):
#         player.make_raise(table, raise_amount)


def test_raise_with_insufficient_chips():
    player = Player(chips=30)
    table = Table()
    table.current_rate = 100
    raise_amount = 50
    table.stake = 300
    with pytest.raises(NotEnoughChipsToPlayError):
        player.make_raise(table, raise_amount)


def test_player_makes_raise_when_current_rate_bigger_than_in_game_chips():
    player = Player(chips=560)
    table = Table()
    player.in_game_chips = 8
    table.current_rate = 16
    raise_amount = 16
    table.stake = 48

    player.make_raise(table, raise_amount)

    assert table.current_rate == 32
    assert table.stake == 48 + 24

    assert player._chips == 560 - 24
    assert player._in_game_chips == 32


def test_player_makes_raise_with_insufficient_chips():
    player = Player(chips=1000)
    table = Table()
    player._chips = 50
    raise_amount = 100
    table.current_rate = 200
    table.stake = 300

    with pytest.raises(NotEnoughChipsToPlayError):
        player.make_raise(table, raise_amount)
