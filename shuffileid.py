from random import Random
from typing import List


class ShuffleID:
    """An algorithm to shuffle an unsigned integer.

    Each integer in a range of 2**bit_size should map to exactly one other integer in the same range. The 
    operation can be efficiently reversed.

    """

    def __init__(self, bit_size: int, shuffles: List[List[int]]) -> None:
        self.bit_size = bit_size
        self.shuffles = shuffles

        self._size = bit_size // 2
        self._x_mask = (2 ** self._size) - 1
        self._y_mask = self._x_mask << self._size
        self._max_shuffle = 2 ** self._size

    @classmethod
    def from_seed(cls, bit_size: int, seed: int, rounds: int = 5) -> "ShuffleID":
        """Initialize from a random seed (the 'secret')."""
        max_shuffle = 2 ** (bit_size // 2)
        size = 2 ** (bit_size // 2) * 2
        randrange = Random(seed).randrange
        shuffles = [
            [randrange(max_shuffle) for _ in range(size)] for _round in range(rounds)
        ]
        return cls(bit_size, shuffles)

    def encode(self, value: int) -> int:
        """Encode an integer."""

        size = self._size

        x = value & self._x_mask
        y = (value & self._y_mask) >> size
        max_shuffle = self._max_shuffle

        for shuffle in self.shuffles:
            x = (x + shuffle[y]) % max_shuffle
            y = (y + shuffle[x + size]) % max_shuffle

        encoded = (y << size) | x
        return encoded

    def decode(self, value: int) -> int:
        """Decode an integer."""

        size = self._size

        x = value & self._x_mask
        y = (value & self._y_mask) >> size
        max_shuffle = self._max_shuffle

        for shuffle in reversed(self.shuffles):
            y = (y - shuffle[x + size]) % max_shuffle
            x = (x - shuffle[y]) % max_shuffle

        encoded = (y << size) | x
        return encoded


if __name__ == "__main__":

    from rich import print
    from rich.columns import Columns
    from rich.color import Color
    from rich.color_triplet import ColorTriplet
    from rich.panel import Panel
    from rich.style import Style
    from rich.text import Text
    from rich.table import Table

    styles = [
        Style(
            bold=True,
            color=Color.from_triplet(ColorTriplet((15 - n) * 16, n * 16, 255)),
        )
        for n in range(16)
    ]

    columns = Columns()

    def render_numbers(numbers, name):
        grid = Table.grid(padding=1)

        for row in range(16):
            row = [
                Text(
                    str(numbers[row * 16 + col]),
                    style=styles[numbers[row * 16 + col] % 16],
                )
                for col in range(16)
            ]
            grid.add_row(*row)
        columns.add_renderable(Panel.fit(grid, title=name))

    numbers = list(range(256))
    render_numbers(numbers, "Ordered")

    shuffle_id = ShuffleID.from_seed(8, 5, rounds=5)
    shuffled = [shuffle_id.encode(value) for value in range(256)]

    render_numbers(shuffled, "Shuffled")

    decoded = [shuffle_id.decode(value) for value in shuffled]
    render_numbers(decoded, "Unshuffled")

    print(columns)
