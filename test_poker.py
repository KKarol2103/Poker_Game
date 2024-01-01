from card import Card, Color, Value
from table import Table
from deck import Deck
from player import Player, AIPlayer
from game import Game
import copy
import random
import pytest


def test_create_a_basic_card():
    my_card = Card(Value.ACE, Color.SPADES)
    assert my_card.__repr__() == "ACE of SPADES"


def test_compare_two_cards():
    my_card = Card(Value.TWO, Color.SPADES)
    my_sec_card = Card(Value.FIVE, Color.SPADES)
    assert my_card < my_sec_card


def test_compare_two_cards_gt():
    my_card = Card(Value.QUEEN, Color.SPADES)
    my_sec_card = Card(Value.JACK, Color.SPADES)
    assert my_card > my_sec_card


def test_check_if_values_are_equal():
    my_val1 = Value.FIVE
    my_val2 = Value.FIVE
    assert my_val1 == my_val2


def test_init_cards_used_in_game():
    play_deck = Deck()
    colors_in_game_count = {}
    for card in play_deck.cards_in_game:
        colors_in_game_count[card.color.name] = colors_in_game_count.get(card.color.name, 0) + 1

    assert colors_in_game_count[Color.SPADES.name] == 13
    assert colors_in_game_count[Color.CLUBS.name] == 13
    assert colors_in_game_count[Color.DIAMONDS.name] == 13
    assert colors_in_game_count[Color.HEARTS.name] == 13


def test_shuffle_cards():
    play_deck = Deck()
    before_shuffle = copy.copy(play_deck.cards_in_game)
    play_deck.tass_cards()
    after = play_deck.cards_in_game
    assert before_shuffle != after


def test_get_round_name():
    new_game = Game()
    new_game.round = 3
    assert new_game.get_current_round_name() == "Turn"


def test_incorrect_round_name():
    new_game = Game()
    new_game.round = 6
    with pytest.raises(ValueError):
        new_game.get_current_round_name()


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


def test_draw_hole_cards():
    deck = Deck()
    new_player = Player()
    new_player.hole_cards = deck.draw_player_hole_cards()
    assert len(deck.cards_in_game) == 50


# def test_attempt_to_give_player_more_cards():
#     deck = Deck()
#     new_player = Player()
#     new_player.hole_cards = deck.draw_player_hole_cards()
#     with pytest.raises(ValueError):
#         new_player.hole_cards = deck.draw_player_hole_cards()


def test_put_cards_on_the_table_flop():
    deck = Deck()
    game_table = Table()
    deck.put_cards_on_the_table(2, game_table)
    assert len(game_table.community_cards) == 3


def test_put_cards_on_the_table_all_rounds():
    deck = Deck()
    game_table = Table()
    deck.put_cards_on_the_table(2, game_table)
    deck.put_cards_on_the_table(3, game_table)
    deck.put_cards_on_the_table(4, game_table)

    assert len(game_table.community_cards) == 5
    assert len(deck.cards_in_game) == 47


def test_try_to_put_wrong_round():
    deck = Deck()
    game_table = Table()
    with pytest.raises(ValueError):
        deck.put_cards_on_the_table(5, game_table)


def test_print_table():
    game_table = Table()
    game_deck = Deck()
    game_deck.put_cards_on_the_table(2, game_table)
    print(game_deck)


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


def mock_compute_player_score(self, table):
    if isinstance(self, Player):
        return 6
    else:
        return 4


def test_get_winer(monkeypatch):
    game = Game()
    monkeypatch.setattr(Player, "compute_player_score", mock_compute_player_score)
    monkeypatch.setattr(AIPlayer, "compute_player_score", mock_compute_player_score)
    normal_player = Player(0, "Gracz")
    first_ai_player = AIPlayer(1)
    second_ai_player = AIPlayer(2)
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]
    winner, score = game.get_winner()
    assert winner.name == "Gracz"
    assert score == 6


def test_get_current_player():
    game = Game()
    normal_player = Player(0, "Gracz")
    first_ai_player = AIPlayer(1)
    second_ai_player = AIPlayer(2)
    game.players_in_game = [normal_player, first_ai_player, second_ai_player]

    game.get_current_player()
    assert game.players_in_game == [first_ai_player, second_ai_player, normal_player]
    game.get_current_player()
    assert game.players_in_game == [second_ai_player, normal_player, first_ai_player]
    game.get_current_player()
    assert game.players_in_game == [normal_player, first_ai_player, second_ai_player]


def test_player_call():
    game = Game()
    normal_player = Player(0, "Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 700
    normal_player._chips = 500
    normal_player._in_game_chips = 100

    normal_player.call(game._game_table)
    assert normal_player.chips == 200
    assert normal_player.in_game_chips == 400


def test_player_check():
    game = Game()
    normal_player = Player(0, "Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 1400
    normal_player._chips = 500
    normal_player._in_game_chips = 400
    normal_player.check(game._game_table)


def test_attempt_to_check_when_rate_is_bigger_than_player_chips():
    game = Game()
    normal_player = Player(0, "Gracz")
    game._game_table.current_rate = 400
    game._game_table.stake = 1400
    normal_player._chips = 500
    normal_player._in_game_chips = 200
    with pytest.raises(ValueError):
        normal_player.check(game._game_table)


def test_player_make_raise():
    game = Game()
    normal_player = Player(0, "Gracz")
    game._game_table.current_rate = 200
    game._game_table.stake = 300
    normal_player._chips = 500
    normal_player._in_game_chips = 200
    normal_player.make_raise(game._game_table, 200)
    assert game._game_table.current_rate == 400
    assert game._game_table.stake == 500
    assert normal_player._chips == 300
    assert normal_player._in_game_chips == 400


def test_player_makes_raise_2():
    player = Player(chips=1000)
    table = Table()
    initial_chips = player._chips
    raise_amount = 100
    table.current_rate = 200
    table.stake = 300

    player.make_raise(table, raise_amount)

    assert table.current_rate == 200 + raise_amount
    assert table.stake == 300 + raise_amount

    assert player._chips == initial_chips - raise_amount
    assert player._in_game_chips == table.current_rate


def test_player_makes_raise_with_insufficient_chips():
    player = Player(chips=1000)
    table = Table()
    player._chips = 50
    raise_amount = 100
    table.current_rate = 200
    table.stake = 300

    with pytest.raises(ValueError):
        player.make_raise(table, raise_amount)


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


def test_aiplayer_raise():
    ai_player = AIPlayer("AIPlayer", chips=1000)
    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.KING, Color.CLUBS), Card(Value.KING, Color.DIAMONDS), Card(Value.KING, Color.CLUBS)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table) == 4


def test_aiplayer_call():
    ai_player = AIPlayer("AIPlayer", chips=1000)
    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.KING, Color.CLUBS), Card(Value.KING, Color.DIAMONDS), Card(Value.KING, Color.CLUBS)]
    ai_player._in_game_chips = 100
    ai_player._chips = 100
    assert ai_player.decide_what_to_do(game_table) == 2


def test_aiplayer_check():
    ai_player = AIPlayer("AIPlayer", chips=1000)

    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.TWO, Color.DIAMONDS), Card(Value.FIVE, Color.CLUBS), Card(Value.ACE, Color.SPADES)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table) == 3


def test_aiplayer_fold():
    ai_player = AIPlayer("AIPlayer", chips=1000)

    game_table = Table()
    game_table.community_cards = []
    game_table.current_rate = 100
    game_table.community_cards = [Card(Value.TWO, Color.DIAMONDS), Card(Value.FIVE, Color.CLUBS), Card(Value.ACE, Color.SPADES), Card(Value.JACK, Color.SPADES)]
    ai_player._in_game_chips = 100
    assert ai_player.decide_what_to_do(game_table) == 1
