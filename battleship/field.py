from typing import Iterator, List

from battleship.cell import Cell


class Field(list):
    """Игровое поле."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        super().__init__(
            [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        )

    def as_transposed(self) -> Iterator[List[Cell]]:
        """Итерирование по транспонированному полю.

        Нужно для удобной проверки как горизонтальных, так и вертикальных
        положений кораблей.
        """
        yield from zip(*self)
