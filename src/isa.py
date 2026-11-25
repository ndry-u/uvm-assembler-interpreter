"""Спецификация команд УВМ (Вариант 20)."""

OPCODE_LOAD = 9
OPCODE_READ = 29
OPCODE_WRITE = 25
OPCODE_MOD = 22

COMMAND_SIZE = 6


def pack_instruction(a: int, b: int, c: int, d: int) -> bytes:
    """Упаковывает поля команды в 6 байт (48 бит)."""
    packed = (a << 0) | (b << 5) | (c << 11) | (d << 29)
    return packed.to_bytes(COMMAND_SIZE, byteorder="little")
