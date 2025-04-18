from enum import Enum


class Color(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

    def __str__(self) -> str:
        color_symbols = {
            Color.HEARTS: "♥",
            Color.DIAMONDS: "♦",
            Color.CLUBS: "♣",
            Color.SPADES: "♠"
        }
        return color_symbols[self]


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

    def __str__(self) -> str:
        return self.symbol


class Card:
    def __init__(self, rank: Value, color: Color) -> None:
        self._color = color
        self._rank = rank

    @property
    def color(self) -> Color:
        return self._color

    @property
    def rank(self) -> Value:
        return self._rank

    def __lt__(self, other):
        return self._rank.number < other.rank.number

    def __gt__(self, other):
        return self._rank.number > other.rank.number

    def __repr__(self):
        return f"{self._rank.name} of {self._color.name}"

    def __str__(self) -> str:
        return f"{str(self._rank)} {str(self._color)}"
