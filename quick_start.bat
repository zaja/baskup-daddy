@echo off
echo ========================================
echo Backup Daddy - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo.
echo Starting application...
echo.
python main.py

pause
