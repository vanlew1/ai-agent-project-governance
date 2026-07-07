@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    python scripts\init_new_project.py
    goto end
)

where py >nul 2>nul
if %errorlevel%==0 (
    py scripts\init_new_project.py
    goto end
)

echo [ERROR] Python was not found on this machine.

echo Please install Python first, then run this file again.

:end
pause
