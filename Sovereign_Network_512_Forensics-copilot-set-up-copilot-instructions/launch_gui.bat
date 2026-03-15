@echo off
setlocal
REM Thin wrapper to use the updated portable launcher
set SCRIPT_DIR=%~dp0

echo 🌌 Launching Erryn's Soul via portable launcher
echo.

if exist "%SCRIPT_DIR%launch_portable.bat" (
    echo ➤ Delegating to: "%SCRIPT_DIR%launch_portable.bat"
    call "%SCRIPT_DIR%launch_portable.bat"
) else (
    echo ❌ launch_portable.bat not found in: "%SCRIPT_DIR%"
    echo    Please run the portable launcher directly or restore the file.
    pause
    exit /b 1
)

endlocal
