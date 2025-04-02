from card import Color
from deck import Deck
import copy


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
    play_deck.shuffle_cards()
    after = play_deck.cards_in_game
    assert before_shuffle != after
