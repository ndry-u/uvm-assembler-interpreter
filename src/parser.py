"""Парсер языка ассемблера УВМ."""

from __future__ import annotations

from dataclasses import dataclass

from src.isa import (
    OPCODE_LOAD,
    OPCODE_MOD,
    OPCODE_READ,
    OPCODE_WRITE,
)

LOAD_ARGS_COUNT = 2
READ_ARGS_COUNT = 2
WRITE_ARGS_COUNT = 2
MOD_ARGS_COUNT = 3


class ParseError(Exception):
    """Ошибка разбора ассемблера."""


@dataclass
class Instruction:
    """Внутреннее представление одной команды."""

    opcode: int
    b: int
    c: int
    d: int


def _extract_args(line: str, mnemonic_length: int) -> list[int]:
    """Извлекает числовые аргументы из строки."""
    args_str = line[mnemonic_length:].strip()
    try:
        return [int(x.strip()) for x in args_str.split(",")]
    except ValueError as error:
        raise ParseError(f"Неверные аргументы в строке: {line}") from error


def _parse_load(line: str) -> Instruction:
    """Парсит команду load."""
    args = _extract_args(line, len("load"))
    if len(args) != LOAD_ARGS_COUNT:
        raise ParseError("load требует 2 аргумента")
    return Instruction(OPCODE_LOAD, args[0], args[1], 0)


def _parse_read(line: str) -> Instruction:
    """Парсит команду read."""
    args = _extract_args(line, len("read"))
    if len(args) != READ_ARGS_COUNT:
        raise ParseError("read требует 2 аргумента")
    return Instruction(OPCODE_READ, args[0], args[1], 0)


def _parse_write(line: str) -> Instruction:
    """Парсит команду write."""
    args = _extract_args(line, len("write"))
    if len(args) != WRITE_ARGS_COUNT:
        raise ParseError("write требует 2 аргумента")
    return Instruction(OPCODE_WRITE, args[0], args[1], 0)


def _parse_mod(line: str) -> Instruction:
    """Парсит команду mod (B - регистр, C и D - адреса памяти)."""
    args = _extract_args(line, len("mod"))
    if len(args) != MOD_ARGS_COUNT:
        raise ParseError("mod требует 3 аргумента")
    return Instruction(OPCODE_MOD, args[0], args[1], args[2])


def _parse_line(line: str, line_no: int) -> Instruction | None:
    """Парсит одну строку ассемблера."""
    clean_line = line.split(";")[0].strip()
    if not clean_line:
        return None

    parts = clean_line.split()
    mnemonic = parts[0].lower()

    parsers = {
        "load": _parse_load,
        "read": _parse_read,
        "write": _parse_write,
        "mod": _parse_mod,
    }

    parser_func = parsers.get(mnemonic)
    if not parser_func:
        raise ParseError(f"Строка {line_no}: неизвестная команда '{mnemonic}'")

    try:
        return parser_func(clean_line)
    except ParseError as error:
        raise ParseError(f"Строка {line_no}: {error}") from error


def parse_program(lines: list[str]) -> list[Instruction]:
    """Превращает список строк в список команд."""
    instructions: list[Instruction] = []
    for i, line in enumerate(lines, start=1):
        instr = _parse_line(line, i)
        if instr:
            instructions.append(instr)
    return instructions
