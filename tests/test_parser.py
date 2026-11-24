"""Тесты для парсера ассемблера УВМ."""

import pytest

from src.isa import OPCODE_LOAD, OPCODE_MOD, OPCODE_READ, OPCODE_WRITE
from src.parser import Instruction, ParseError, parse_program

EXPECTED_INSTRUCTIONS = 4
EXPECTED_TWO_COMMANDS = 2


class TestParseProgram:
    """Тесты функции parse_program."""

    def test_parse_valid_program(self) -> None:
        """Парсит все 4 команды из спецификации."""
        lines = [
            "load 4, 758",
            "read 49, 170",
            "write 5, 119",
            "mod 48, 22, 957",
        ]
        result = parse_program(lines)
        assert len(result) == EXPECTED_INSTRUCTIONS

        assert result[0] == Instruction(OPCODE_LOAD, 4, 758, 0)
        assert result[1] == Instruction(OPCODE_READ, 49, 170, 0)
        assert result[2] == Instruction(OPCODE_WRITE, 5, 119, 0)
        assert result[3] == Instruction(OPCODE_MOD, 48, 22, 957)

    def test_parse_with_comments_and_spaces(self) -> None:
        """Игнорирует комментарии и пустые строки."""
        lines = [
            "  load 4, 758 ; загрузка ",
            "",
            "; просто комментарий",
            "  ",
            "read 5, 170",
        ]
        result = parse_program(lines)
        assert len(result) == EXPECTED_TWO_COMMANDS
        assert result[0].opcode == OPCODE_LOAD
        assert result[1].opcode == OPCODE_READ

    def test_unknown_command(self) -> None:
        """Выбрасывает ошибку на неизвестной команде."""
        lines = ["unknown_cmd 1, 2"]
        with pytest.raises(ParseError):
            parse_program(lines)

    def test_wrong_args_count(self) -> None:
        """Выбрасывает ошибку при неверном числе аргументов."""
        lines = ["load 4"]
        with pytest.raises(ParseError):
            parse_program(lines)

    def test_invalid_args_type(self) -> None:
        """Выбрасывает ошибку, если аргументы не числа."""
        lines = ["load a, b"]
        with pytest.raises(ParseError):
            parse_program(lines)
