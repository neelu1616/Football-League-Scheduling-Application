@echo off
REM Football League Management System - Windows Launcher
REM Double-click this file to start the application

echo.
echo ============================================================
echo   Football League Management System
echo   Starting...
echo ============================================================
echo.

python start.py

if errorlevel 1 (
    echo.
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
)
