import pytest

from battleship import compressor
from battleship.battleship import MoveResult


@pytest.mark.parametrize(
    "cell_x, cell_y", [(0, 0), (0, 1), (1, 0), (1, 1), (10, 10)]
)
def test_coords(cell_x, cell_y):
    assert compressor.decomress_coords(
        compressor.compress_coords(cell_x, cell_y)
    ) == (cell_x, cell_y)


@pytest.mark.parametrize(
    "move_result",
    [
        MoveResult.MISS,
        MoveResult.DAMAGED,
        MoveResult.DESTROYED,
        MoveResult.WIN,
    ],
)
def test_move_result(move_result):
    assert compressor.decompress_move_result(
        compressor.compress_move_result(move_result)
    ) == move_result
