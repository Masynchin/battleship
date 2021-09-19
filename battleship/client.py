import socket

from battleship import const
from battleship.exceptions import CouldNotConfirmError


class Client:
    def _send(self, data: bytes):
        """Отправка данных другой стороне."""
        self._client_socket.sendall(data)

    def _receive(self, data_length: int) -> bytes:
        """Получение данных от другой стороны."""
        return self._client_socket.recv(data_length)


class SubClient(Client):
    """Клиент."""

    def __init__(self, server_host: str):
        self._server_host = server_host
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handshake(self):
        """Хэндшейк."""
        self._send_confirm()
        self._accept_confirm()

    def _accept_confirm(self):
        """Подтверждение согласия на соединение с другой стороной."""
        response = self._receive(const.CONFIRM_MESSAGE_SIZE)
        if response != const.MSG_SERVER_CONF:
            raise CouldNotConfirmError(
                "Сервер не подтвердил соглашение на соединение."
            )

    def _send_confirm(self):
        """Отправка согласия на соединение другой стороне."""
        self._send(const.MSG_CLIENT_CONF)

    def connect_to_server(self):
        """Подключение к серверу."""
        self._client_socket.connect((self._server_host, const.PORT))

    def close(self):
        """Закрытие клиента."""
        self._client_socket.close()


class MainClient(Client):
    """Сервер."""

    def __init__(self):
        self._host = socket.gethostbyname(socket.gethostname())

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._host, const.PORT))

        self._client_socket = None

    def get_host(self) -> str:
        """Получение названия хоста."""
        return self._host

    def listen_and_connect_to_client(self):
        """Подключение к клиенту."""
        self._server_socket.listen()
        self._client_socket, _ = self._server_socket.accept()

    def handshake(self):
        """Хэндшейк."""
        self._accept_confirm()
        self._send_confirm()

    def _accept_confirm(self):
        """Подтверждение согласия на соединение с другой стороной."""
        response = self._receive(const.CONFIRM_MESSAGE_SIZE)
        if response != const.MSG_CLIENT_CONF:
            raise CouldNotConfirmError(
                "Клиент не подтвердил соглашение на соединение."
            )

    def _send_confirm(self):
        """Отправка согласия на соединение другой стороне."""
        self._send(const.MSG_SERVER_CONF)

    def close(self):
        """Закрытие сервера."""
        self._client_socket.close()
        self._server_socket.close()
