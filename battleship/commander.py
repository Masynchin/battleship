from typing import Tuple

from battleship import const
from battleship.client import Client, MainClient, SubClient
from battleship.compressor import (
    compress_coords,
    decomress_coords,
    compress_move_result,
    decompress_move_result,
)
from battleship.battleship import MoveResult


class Commander(Client):
    """Командир.

    Класс предоставляет общие методы для общения данными как для сервера,
    так и для клиента.
    """

    def send_coords(self, cell_x: int, cell_y: int):
        """Отправка координат хода другой стороне."""
        message = compress_coords(cell_x, cell_y)
        self._send(message)

    def receive_coords(self) -> Tuple[int, int]:
        """Получение координат хода от другой стороны."""
        message = self._receive(const.MOVE_COORDS_MESSAGE_SIZE)
        cell_x, cell_y = decomress_coords(message)
        return cell_x, cell_y

    def send_move_result(self, move_result: MoveResult):
        """Отправка результата хода другой стороне."""
        message = compress_move_result(move_result)
        self._send(message)

    def receive_move_result(self) -> MoveResult:
        """Получение результата хода от другой стороны."""
        message = self._receive(const.MOVE_RESULT_MESSAGE_SIZE)
        move_result = decompress_move_result(message)
        return move_result


class MainCommander(MainClient, Commander):
    """Командир-сервер."""


class SubCommander(SubClient, Commander):
    """Командир-клиент."""
