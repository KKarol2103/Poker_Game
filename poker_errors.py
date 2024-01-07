class SinglePlayerWantsToFoldError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Can't fold when there is only one player!")


class NotEnoughChipsToPlayError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Not enough chips to play!")


class InvalidActionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid Option!")


class InvalidAmountCheckError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Can't check when you don't have same chips as others")


class InvalidInputData(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Incorrect data given")


class InvalidRoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid Round")
