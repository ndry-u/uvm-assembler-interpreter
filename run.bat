@echo off
rem Использование:
rem   run.bat test        - запустить тесты
rem   run.bat <аргументы> - передать аргументы ассемблеру
chcp 65001 >nul

if "%~1"=="test" (
    python -m pytest -v
) else (
    python -m src.main %*
)
