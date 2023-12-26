from card import Card, Color, Value
from deck import Deck
from player import Player, AIPlayer
from game import Game
import copy
import pytest


def test_create_a_basic_card():
    my_card = Card(Value.ACE, Color.SPADES,)
    assert my_card.__repr__() == "ACE of SPADES"


def test_init_cards_used_in_game():
    play_deck = Deck()
    play_deck.init_cards_used_in_a_game()
    colors_in_game_count = {}
    for card in play_deck.cards_in_game:
        colors_in_game_count[card.color.name] = colors_in_game_count.get(card.color.name, 0) + 1

    assert colors_in_game_count[Color.SPADES.name] == 13
    assert colors_in_game_count[Color.CLUBS.name] == 13
    assert colors_in_game_count[Color.DIAMONDS.name] == 13
    assert colors_in_game_count[Color.HEARTS.name] == 13


def test_shuffle_cards():
    play_deck = Deck()
    play_deck.init_cards_used_in_a_game()
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


def mock_sample(start, end):
    return start


def test_draw_the_order_of_players():
    new_game = Game()
    new_game.players_in_game = [Player(), AIPlayer(), AIPlayer(), AIPlayer()]
    new_game.draw_the_order_of_players()
    expected_order = [1, 2, 3, 4]
    # monkeypatch.setattr("random.randint", mock_sample)
    actual_order = [player.player_num for player in new_game._players_in_game]
