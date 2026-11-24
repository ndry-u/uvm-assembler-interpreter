"""Ассемблер УВМ (Этап 1)."""

from __future__ import annotations

import argparse
import sys

from src.parser import ParseError, parse_program


def build_parser() -> argparse.ArgumentParser:
    """Создаёт argparse-парсер."""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("--input", required=True, help="Путь к файлу .asm")
    parser.add_argument(
        "--output", required=True, help="Путь к бинарному файлу"
    )
    parser.add_argument(
        "--test-mode", action="store_true", help="Режим тестирования"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Точка входа."""
    args = build_parser().parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            lines = f.readlines()
        instructions = parse_program(lines)
    except FileNotFoundError:
        print(f"Файл не найден: {args.input}", file=sys.stderr)
        return 1
    except ParseError as error:
        print(f"Ошибка разбора: {error}", file=sys.stderr)
        return 1

    if args.test_mode:
        print("Внутреннее представление программы:")
        for i, instr in enumerate(instructions):
            print(
                f"  {i}: A={instr.opcode}, B={instr.b}, "
                f"C={instr.c}, D={instr.d}"
            )

    print(f"\nУспешно разобрано команд: {len(instructions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
