import itertools as it
from typing import Tuple

from battleship.cell import Cell, CellType
from battleship.field import Field
from battleship.battleship import MoveResult


def compress_field(field: Field) -> bytes:
    """Превращение игрового поля в байтовые данные."""
    cells_data = (_comress_cell(cell) for row in field for cell in row)
    width_data = _compress_number(field.width)
    height_data = _compress_number(field.height)

    return b"".join(it.chain((width_data, height_data), cells_data))


def decompress_field(field_data: bytes) -> Field:
    """Получение игрового поля из байтовых данных."""
    width, height, *cells = field_data

    field = Field(width, height)
    for j in range(height):
        for i, cell in enumerate(cells[j*width:(j+1)*width]):
            cell = _decomress_cell(cell)
            field[j][i] = cell

    return field


def _comress_cell(cell: Cell) -> bytes:
    """Превращение клетки игрового поля в байтовые данные."""
    return _compress_number(cell.type)


def _decomress_cell(cell_data: int) -> Cell:
    """Получение клетки игрового поля из числовых данных."""
    cell_type = CellType.DEFAULT
    i = 0
    while (factor := 2**i) <= cell_data:
        if factor & cell_data:
            cell_type |= CellType(factor)
        i += 1

    return Cell(cell_type)


def _compress_number(number: int) -> bytes:
    """Превращение числа в байты."""
    return number.to_bytes((number.bit_length() + 7) // 8, byteorder="big")


def _decompress_number(number_data: bytes) -> int:
    """Получение числа из байт."""
    return int.from_bytes(number_data, byteorder="big")


def compress_coords(cell_x: int, cell_y: int) -> bytes:
    """Превращение координат клетки в байтовые данные."""
    # добавление единицы нужно для того, чтобы число 0 имело байтовое
    # представление (изначально, он выдаёт b"")
    return b"".join((_compress_number(cell_x+1), _compress_number(cell_y+1)))


def decomress_coords(coords_data: bytes) -> Tuple[int, int]:
    """Получение координат клетки из байтовых данных."""
    cell_x, cell_y = coords_data
    # вычитание единицы происходит вследствие работы `compress_coords`
    return cell_x-1, cell_y-1


def compress_move_result(move_result: MoveResult) -> bytes:
    """Превращение результата хода в байтовые данные."""
    return _compress_number(int(move_result))


def decompress_move_result(move_result_data: bytes) -> MoveResult:
    """Получение результата хода из байтовых данных."""
    return MoveResult(_decompress_number(move_result_data))
