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

