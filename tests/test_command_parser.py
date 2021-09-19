import pytest

from battleship.command_parser import parse_command
from battleship.exceptions import InvalidCommand


@pytest.mark.parametrize(
    "command",
    [
        "1 A",  # англ.
        "1 Ё",  # буква вне диапазона колонок
        "А А",  # плохое число
        "1 1",  # плохая буква
    ],
)
def test_invalid_command(command):
    with pytest.raises(InvalidCommand):
        parse_command(command)


@pytest.mark.parametrize(
    "command, expected",
    [
        ("1 А", (0, 0)),
        ("2 Б", (1, 1)),
        ("2 А", (0, 1)),
        ("1 Б", (1, 0)),
        ("5 К", (9, 4)),
    ],
)
def test_valid_command(command, expected):
    assert parse_command(command) == expected
