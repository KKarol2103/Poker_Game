from card import Card, Color, Value
from deck import Deck


def test_create_a_basic_card():
    Card(Value.ACE, Color.SPADES,)


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

