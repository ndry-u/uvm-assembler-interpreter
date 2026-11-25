"""Генератор машинного кода УВМ."""

from __future__ import annotations

from src.isa import pack_instruction
from src.parser import Instruction


def generate_binary(instructions: list[Instruction]) -> bytes:
    """Превращает список инструкций в последовательность байт."""
    result = bytearray()
    for instr in instructions:
        binary_instr = pack_instruction(
            instr.opcode, instr.b, instr.c, instr.d
        )
        result.extend(binary_instr)
    return bytes(result)


def format_bytes_hex(data: bytes) -> str:
    """Форматирует байты в строку вида '0x89, 0xB0, 0x17...'."""
    return ", ".join(f"0x{b:02X}" for b in data)
