@echo off
setlocal
set "BASE=%~dp0"
set "APP=%BASE%erryns_soul_gui_v3_sync_monitor.py"
set "VENV=%BASE%.venv"
set "PYVENV=%VENV%\Scripts\python.exe"

rem Find python
set "PYCMD="
if exist "%PYVENV%" set "PYCMD=%PYVENV%"
if not defined PYCMD (
  for %%P in (py.exe python.exe) do (
    where %%P >nul 2>nul && set "PYCMD=%%P" && goto :found
  )
)
:found
if not defined PYCMD (
  echo [!] Python 3.11+ not found. Please install Python and rerun.
  pause
  exit /b 1
)

rem Create venv if missing
if not exist "%PYVENV%" (
  %PYCMD% -m venv "%VENV%"
)
set "PYRUN=%PYVENV%"

rem Install deps
"%PYRUN%" -m pip install -r "%BASE%requirements.txt" >nul 2>nul

rem Run app: prefer local copy; fallback to Desktop
if not exist "%APP%" (
  set "APP=C:\Users\stu43\OneDrive\Desktop\erryns_soul_gui_v3_sync_monitor.py"
)

if not exist "%APP%" (
  echo [!] App file not found:
  echo     %APP%
  echo Place the GUI script next to this launcher or update APP path.
  pause
  exit /b 1
)

echo 🚀 Starting GUI from: %APP%
"%PYVENV%" "%APP%"
exit /b 0
