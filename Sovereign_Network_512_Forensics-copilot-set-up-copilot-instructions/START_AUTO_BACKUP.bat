@echo off
REM Auto Git Backup Launcher
REM Run this to start automatic 5-minute backups

setlocal enabledelayedexpansion

REM Get current directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if .git exists
if not exist .git (
    echo.
    echo ❌ ERROR: Not a git repository!
    echo.
    echo Run this first:
    echo   git init
    echo   git config user.name "Stuart"
    echo   git config user.email "your@email.com"
    echo   git add .
    echo   git commit -m "Initial commit"
    echo.
    pause
    exit /b 1
)

REM Check if venv is activated, if not activate it
if not defined VIRTUAL_ENV (
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    )
)

REM Run auto-backup
python auto_git_backup.py 5

pause
