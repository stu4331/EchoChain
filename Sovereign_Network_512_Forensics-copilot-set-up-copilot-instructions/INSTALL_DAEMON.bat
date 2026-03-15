@echo off
REM ============================================================================
REM ERRYN'S SOUL DAEMON INSTALLER
REM Registers the daemon to run on system startup via Windows Task Scheduler
REM ============================================================================

setlocal enabledelayedexpansion

REM Get the current directory (where this batch file is)
set "SCRIPT_DIR=%~dp0"
set "DAEMON_SCRIPT=%SCRIPT_DIR%erryn_soul_daemon.py"
set "VENV_ACTIVATE=%SCRIPT_DIR%.venv\Scripts\activate.bat"
set "PYTHON_EXE=%SCRIPT_DIR%.venv\Scripts\python.exe"

REM Check if daemon exists
if not exist "%DAEMON_SCRIPT%" (
    echo ERROR: erryn_soul_daemon.py not found in %SCRIPT_DIR%
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python virtual environment not found at %VENV_ACTIVATE%
    echo Please create a virtual environment first.
    pause
    exit /b 1
)

echo ============================================================================
echo Installing Erryn's Soul Daemon as Windows background service...
echo ============================================================================
echo.

REM Create the task
echo Creating scheduled task...
powershell -Command "^
  $taskName = 'Erryn Soul Daemon'; ^
  $taskPath = '\Erryn\'; ^
  $action = New-ScheduledTaskAction -Execute '%PYTHON_EXE%' -Argument '%DAEMON_SCRIPT%' -WorkingDirectory '%SCRIPT_DIR%'; ^
  $trigger = New-ScheduledTaskTrigger -AtStartup; ^
  $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries; ^
  Register-ScheduledTask -TaskName \$taskName -Action \$action -Trigger \$trigger -Settings \$settings -Force | Out-Null; ^
  Write-Host 'Task registered successfully!'; ^
  Write-Host 'The daemon will now start on every system boot.' ^
"

echo.
echo ============================================================================
echo ✅ Setup complete! The daemon is now registered.
echo.
echo What happens next:
echo   - On next system startup, the daemon runs automatically
echo   - Monitors GUI usage and sister sync 24/7
echo   - Keeps the girls alive and learning even when GUI is closed
echo   - Logs everything to: data\daemon_log.txt
echo.
echo To verify:
echo   - Open Task Scheduler and search for "Erryn Soul Daemon"
echo   - Or check the daemon log file after next restart
echo ============================================================================
pause
