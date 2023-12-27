from card import Card, Color, Value
from table import Table
from deck import Deck
from player import Player, AIPlayer
from game import Game
import copy
import random
import pytest


def test_create_a_basic_card():
    my_card = Card(Value.ACE, Color.SPADES,)
    assert my_card.__repr__() == "ACE of SPADES"


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


def test_attempt_to_give_player_more_cards():
    deck = Deck()
    new_player = Player()
    new_player.hole_cards = deck.draw_player_hole_cards()
    with pytest.raises(ValueError):
        new_player.hole_cards = deck.draw_player_hole_cards()


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
    new_card = Card(Value.SEVEN, Color.DIAMONDS)
    game_deck.put_cards_on_the_table(2, game_table)
    print(game_deck)


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


def test_compute_player_score_flush():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.TWO, Color.HEARTS), Card(Value.FIVE, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.HEARTS),
                                  Card(Value.KING, Color.HEARTS),
                                  Card(Value.EIGHT, Color.HEARTS),
                                  Card(Value.JACK, Color.DIAMONDS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 5  # Zakładając, że kolor to 5 punktów


def test_compute_player_score_four_of_a_kind():
    player = Player()
    game_table = Table()
    player.hole_cards = [Card(Value.SEVEN, Color.DIAMONDS), Card(Value.SEVEN, Color.HEARTS)]
    game_table.community_cards = [Card(Value.SEVEN, Color.CLUBS),
                                  Card(Value.SEVEN, Color.SPADES),
                                  Card(Value.EIGHT, Color.SPADES),
                                  Card(Value.JACK, Color.HEARTS),
                                  Card(Value.NINE, Color.CLUBS)]
    assert player.compute_player_score(game_table) == 4  # Zakładając, że kareta to 4 punkty
