from card import Card, Color, Value


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
