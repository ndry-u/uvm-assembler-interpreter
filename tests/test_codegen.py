"""Тесты для генератора машинного кода."""

from src.codegen import format_bytes_hex, generate_binary
from src.isa import OPCODE_LOAD, OPCODE_READ
from src.parser import Instruction

BYTES_IN_COMMAND = 6


class TestGenerateBinary:
    """Тесты функции generate_binary."""

    def test_generate_load(self) -> None:
        """Проверяет байты для команды загрузки константы."""
        instr = Instruction(OPCODE_LOAD, 4, 758, 0)
        binary = generate_binary([instr])
        assert len(binary) == BYTES_IN_COMMAND
        assert binary == bytes([0x89, 0xB0, 0x17, 0x00, 0x00, 0x00])

    def test_generate_multiple(self) -> None:
        """Проверяет длину бинарного файла для нескольких команд."""
        instrs = [
            Instruction(OPCODE_LOAD, 4, 758, 0),
            Instruction(OPCODE_READ, 49, 170, 0),
        ]
        binary = generate_binary(instrs)
        assert len(binary) == BYTES_IN_COMMAND * len(instrs)

    def test_empty_instructions(self) -> None:
        """Пустой список команд дает пустой бинарник."""
        assert generate_binary([]) == b""


class TestFormatBytesHex:
    """Тесты функции format_bytes_hex."""

    def test_format_hex(self) -> None:
        """Проверяет форматирование в 0xXX."""
        data = bytes([0x89, 0xB0])
        assert format_bytes_hex(data) == "0x89, 0xB0"

    def test_empty_bytes(self) -> None:
        """Пустые байты форматируются в пустую строку."""
        assert format_bytes_hex(b"") == ""
