import itertools as it
import random
from enum import IntFlag, auto
from typing import Iterator, Tuple

from battleship.field import Field


class MoveResult(IntFlag):
    """Результат хода."""

    MISS = auto()
    DAMAGED = auto()
    DESTROYED = auto()
    WIN = auto()

    @property
    def is_miss(self) -> bool:
        """Является ли результат хода промахом."""
        return self == MoveResult.MISS

    @property
    def is_damaged(self) -> bool:
        """Является ли результат хода повреждением корабля."""
        return self == MoveResult.DAMAGED

    @property
    def is_destroyed(self) -> bool:
        """Является ли результат хода потоплением корабля."""
        return self == MoveResult.DESTROYED

    @property
    def is_win(self) -> bool:
        """Является ли результат хода победой."""
        return self == MoveResult.WIN


class Battleship:
    """Интерфейс игры."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.field = Field(self.width, self.height)

    def place_ships(self):
        """Размещение кораблей в случайном порядке.

        Весь метод строится на основании, что следуя правилам игры,
        не существует позиций, когда невозможно разместить все корабли.

        Начиная с пустого поля, каждой итерацией мы находим все возможные
        (как горизонтальные, так и вертикальные) положения корабля, размещаем
        корабль, запоминаем координаты, и проходим так до тех пор, пока
        не установлены все корабли.

        Все операции по отметке занятых клеток проводятся на "разметочном"
        поле. После заполнения разметочного поля всеми кораблями, по
        получившимся координатам расставляются корабли на игровом поле.
        """
        mark_field = Field(self.width, self.height)
        ships_points = set()

        ships_with_count = {
            4: 1,
            3: 2,
            2: 3,
            1: 4,
        }
        for (ship_length, ships_count) in ships_with_count.items():
            for _ in range(ships_count):
                ship_points = _get_available_ship_points(
                    mark_field, ship_length
                )
                points = random.choice(tuple(ship_points))
                ships_points.add(points)
                _mark_ship_around_points(mark_field, *points)

        for point in ships_points:
            self._place_ship(*point)

    def _place_ship(self, x0: int, y0: int, x1: int, y1: int):
        """Размещение корабля на игровом поле."""
        for (x, y) in it.product(
            range(x0, x1+1),
            range(y0, y1+1),
            repeat=1,
        ):
            self.field[y][x].set_ship()

    def hit_cell(self, cell_x: int, cell_y: int) -> MoveResult:
        """Обстрел клетки."""
        cell = self.field[cell_y][cell_x]
        if not cell.is_ship:
            move_result = MoveResult.MISS
        else:
            move_result = MoveResult.DAMAGED
            if self._is_ship_destroyed(cell_x, cell_y):
                move_result = MoveResult.DESTROYED
                if self._is_win(cell_x, cell_y):
                    move_result = MoveResult.WIN

        self.update_cell(cell_x, cell_y, move_result)
        return move_result

    def update_cell(self, cell_x: int, cell_y: int, move_result: MoveResult):
        """Обновление клетки в соответствии с результатом хода."""
        cell = self.field[cell_y][cell_x]
        if move_result == MoveResult.MISS:
            cell.set_miss()
        elif move_result == MoveResult.DAMAGED:
            cell.set_damaged()
            # чтобы `get_ship_points` работал и для вражеской карты,
            # клетку нужно обозначить кораблём
            cell.set_ship()
        elif move_result == MoveResult.DESTROYED:
            for (x, y) in self.get_ship_points(cell_x, cell_y):
                self.field[y][x].set_destroyed()

    def get_ship_points(
        self, cell_x: int, cell_y: int
    ) -> Iterator[Tuple[int, int]]:
        """Получение всех клеток корабля.

        Получение клеток корабля, одна из которых находится в
        заданных координатах.
        """
        yield (cell_x, cell_y)

        def filter_func(x: int, y: int) -> bool:
            """Если в точке есть корабль, то это часть искомого корабля."""
            return (
                0 <= x < self.width
                and 0 <= y < self.height
                and self.field[y][x].is_ship
            )

        # поиск клеток корабля справа
        x, y = cell_x + 1, cell_y
        while filter_func(x, y):
            yield (x, y)
            x += 1

        # поиск клеток корабля слева
        x, y = cell_x - 1, cell_y
        while filter_func(x, y):
            yield (x, y)
            x -= 1

        # поиск клеток корабля снизу
        x, y = cell_x, cell_y + 1
        while filter_func(x, y):
            yield (x, y)
            y += 1

        # поиск клеток корабля сверху
        x, y = cell_x, cell_y - 1
        while filter_func(x, y):
            yield (x, y)
            y -= 1

    def _is_ship_destroyed(self, cell_x: int, cell_y: int) -> bool:
        """Является ли корабль потопленным.

        Вызывается во время расчёта результата хода. Так как во время расчёта
        хода клетки поля не изменяются, то существует проверка на то, что
        либо корабль в клетке повреждён, либо клетка является объектом хода
        (тогда все остальные клетки корабля должны быть повреждены).
        """
        return all(
            self.field[y][x].is_damaged or (x, y) == (cell_x, cell_y)
            for (x, y) in self.get_ship_points(cell_x, cell_y)
        )

    def _is_win(self, cell_x: int, cell_y: int) -> bool:
        """Потоплены ли все корабли.

        Вызывается во время расчёта результата хода. Так как во время расчёта
        хода клетки поля не изменяются, то существует проверка, что либо
        корабль потоплен, либо корабль будет потоплен этим ходом.
        """
        return all(
            not cell.is_ship or cell.is_destroyed or (i, j) == (cell_x, cell_y)
            for j, row in enumerate(self.field)
            for i, cell in enumerate(row)
        )


def _get_available_ship_points(
    mask_field: Field, ship_length: int
) -> Iterator[Tuple[int, int, int, int]]:
    """Получение всех возможных точек расположения корабля.

    Получение всех возможных точек расположения для
    горизонтального и вертикального полежения.
    """
    for j, row in enumerate(mask_field):
        prev = 0
        for i, cell in enumerate(row):
            if cell.is_ship:
                prev = 0
            else:
                prev += 1
                if prev >= ship_length:
                    yield (i-ship_length+1, j, i, j)

    for i, row in enumerate(mask_field.as_transposed()):
        prev = 0
        for j, cell in enumerate(row):
            if cell.is_ship:
                prev = 0
            else:
                prev += 1
                if prev >= ship_length:
                    yield (i, j-ship_length+1, i, j)


def _mark_ship_around_points(
    mark_field: Field, x0: int, y0: int, x1: int, y1: int
):
    """Размещение корабля на разметочном поле.

    "Размещая" корабль, мы обозначаем клетки, в которых не могут находиться
    другие корабли - это клетки самого корабля, и его соседние клетки.
    """
    for (x, y) in it.product(
        range(x0-1, x1+2),
        range(y0-1, y1+2),
        repeat=1,
    ):
        if 0 <= x < mark_field.width and 0 <= y < mark_field.height:
            mark_field[y][x].set_ship()
