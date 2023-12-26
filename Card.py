from enum import Enum


class Color(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4


class Value(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")

    def __init__(self, number, symbol):
        self.number = number
        self.symbol = symbol


class Card:
    def __init__(self, value: Value, color: Color) -> None:
        self._color = color
        self._value = value

    @property
    def color(self) -> Color:
        return self._color

    @property
    def value(self) -> Value:
        return self._value

    def __repr__(self):
        return f"{self._value.name} of {self._color.name}"
