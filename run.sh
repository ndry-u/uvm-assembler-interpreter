#!/usr/bin/env sh
# Использование:
#   ./run.sh test        - запустить тесты
#   ./run.sh <аргументы> - передать аргументы ассемблеру
set -eu

if [ "${1:-}" = "test" ]; then
    python3 -m pytest -v
else
    python3 -m src.main "$@"
fi
