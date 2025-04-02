from table import Table
from deck import Deck
from player import Player
import pytest


def test_draw_hole_cards():
    deck = Deck()
    new_player = Player()
    new_player.hole_cards = deck.draw_player_hole_cards()
    assert len(deck.cards_in_game) == 50


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
