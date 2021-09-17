from enum import IntFlag


class CellType(IntFlag):
    """Тип клетки игрового поля."""

    DEFAULT = 1
    SHIP = 2
    MISS = 4
    DAMAGED = 8
    DESTROYED = 16


class Cell:
    """Клетка игрового поля."""

    def __init__(self, cell_type: CellType = CellType.DEFAULT):
        self.type = cell_type

    @property
    def is_ship(self) -> bool:
        """Есть ли корабль в клетке."""
        return self.type & CellType.SHIP

    def set_ship(self):
        """Пришвартовка корабля в клетку."""
        self.type |= CellType.SHIP

    @property
    def is_miss(self) -> bool:
        """Есть ли промах в клетке."""
        return self.type & CellType.MISS

    def set_miss(self):
        """Отметка промаха."""
        self.type |= CellType.MISS

    @property
    def is_damaged(self) -> bool:
        """Есть ли повреждённый корабль в клетке."""
        return self.type & CellType.DAMAGED

    def set_damaged(self):
        """Отметка повреждения корабля."""
        self.type |= CellType.DAMAGED

    @property
    def is_destroyed(self) -> bool:
        """Есть ли потопленный корабль в клетке."""
        return self.type & CellType.DESTROYED

    def set_destroyed(self):
        """Отметка потопления корабля."""
        self.type |= CellType.DESTROYED
