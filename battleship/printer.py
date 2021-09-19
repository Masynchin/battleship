from typing import List

from battleship.cell import Cell
from battleship.field import Field


ROWS_INDEXES = tuple(map(str, range(1, 11)))
COLS_INDEXES = "АБВГДЕЖЗИК"
FIELDS_SEP = "   #   "


def print_fields(player_field: Field, enemy_field: Field):
    """Вывод своего игрового поля и игрового поля соперника в консоль."""
    _print_fields_titles(player_field.width)
    _print_columns()

    for row_index, player_row, enemy_row in zip(
        ROWS_INDEXES, player_field, enemy_field
    ):
        _print_rows(row_index, player_row, enemy_row)


def _print_fields_titles(cells_count: int):
    """Вывод владельцев игровых полей в консоль."""
    # длина ряда состоит из N клеток, N-1 разделителей между ними,
    # и 2 разделителей по краям
    row_width = cells_count * 2 + 1

    # первые 3 пробела это 2 символа индекса рядов и 1 пробел между
    # индексами рядов и самими рядами.
    our_title = " " * 3 + f"{'Ваше поле':^{row_width}}"
    enemy_title = " " * 3 + f"{'Поле соперника':^{row_width}}"
    print(f"{our_title}{FIELDS_SEP}{enemy_title}")


def _print_columns():
    """Вывод букв колонок полей игрока и соперника в консоль."""
    # первые четыре пробела это 2 символа индекса рядов, 1 пробел между
    # индексами рядов и полей, и 1 символ первого разделителя клеток.
    # Последний пробел обозначает последний разделитель клеток.
    column_row = " " * 4 + " ".join(COLS_INDEXES) + " "
    print(f"{column_row}{FIELDS_SEP}{column_row}")


def _print_rows(row_index: str, player_row: List[Cell], enemy_row: List[Cell]):
    """Вывод рядов полей игрока и соперника с их индексами в консоль."""
    player_row = f"{row_index:>2} {_str_row(player_row)}"
    enemy_row = f"{row_index:>2} {_str_row(enemy_row)}"
    print(f"{player_row}{FIELDS_SEP}{enemy_row}")


def _str_row(row: List[Cell]) -> str:
    """Строковое представление ряда игрового поля для вывода в консоль."""
    str_row = "|".join(_str_cell(cell) for cell in row)
    return f"|{str_row}|"


def _str_cell(cell: Cell) -> str:
    """Строковое представление клетки для вывода в консоль."""
    if cell.is_destroyed:
        return "x"
    elif cell.is_damaged:
        return "+"
    elif cell.is_miss:
        return "."
    elif cell.is_ship:
        return "&"
    else:
        return " "
