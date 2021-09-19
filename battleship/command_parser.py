from typing import Tuple

from battleship.exceptions import InvalidCommand
from battleship.printer import COLS_INDEXES, ROWS_INDEXES


def parse_command(command: str) -> Tuple[int, int]:
    """Получение координат хода из ввода игрока."""
    try:
        cell_y, cell_x = command.split()
        cell_x = COLS_INDEXES.index(cell_x)
        cell_y = ROWS_INDEXES.index(cell_y)
    except ValueError:
        raise InvalidCommand("Неправильный вид команды!")
    else:
        return cell_x, cell_y
