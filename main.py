import os
from contextlib import closing
from typing import Tuple

from battleship.commander import Commander, MainCommander, SubCommander
from battleship.command_parser import parse_command
from battleship.exceptions import InvalidCommand
from battleship.printer import print_fields
from battleship.battleship import Battleship


def main():
    mode = None
    while mode not in {"s", "c"}:
        mode = input("Сервер - s, клиент - c: ")

    if mode == "s":
        with closing(MainCommander()) as server:
            print(f"Подключайтесь к {server.get_host()}")

            server.listen_and_connect_to_client()
            server.handshake()
            process_game(server, first_turn=True)

    elif mode == "c":
        server_host = input("Введите адрес сервера: ")
        with closing(SubCommander(server_host)) as client:
            client.connect_to_server()
            client.handshake()
            process_game(client, first_turn=False)


def process_game(channel: Commander, first_turn: bool):
    our_battleship = Battleship(10, 10)
    our_battleship.place_ships()

    enemy_battleship = Battleship(10, 10)

    turn = first_turn
    while True:
        clear_screen()
        print_fields(our_battleship.field, enemy_battleship.field)

        if turn:
            cell_x, cell_y = get_move_coords()
            channel.send_coords(cell_x, cell_y)
            move_result = channel.receive_move_result()

            enemy_battleship.update_cell(cell_x, cell_y, move_result)

            if move_result.is_miss:
                turn = False
            elif move_result.is_win:
                clear_screen()
                print("Вы победили!")
                return

        else:
            cell_x, cell_y = channel.receive_coords()
            move_result = our_battleship.hit_cell(cell_x, cell_y)
            channel.send_move_result(move_result)

            if move_result.is_miss:
                turn = True
            elif move_result.is_win:
                clear_screen()
                print("Вы проиграли!")
                return


def clear_screen():
    os.system("clear")


def get_move_coords() -> Tuple[int, int]:
    """Получение координат хода от игрока."""
    while True:
        try:
            command = input("Введите координаты хода: ")
            cell_x, cell_y = parse_command(command)
        except InvalidCommand:
            print("Неверный формат ввода!")
        else:
            return cell_x, cell_y


if __name__ == "__main__":
    main()
