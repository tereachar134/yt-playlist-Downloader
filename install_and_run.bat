@echo off
set "VENV_DIR=venv"

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to your PATH.
    pause
    exit /b
)

rem Create virtual environment if it doesn't exist
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

rem Activate virtual environment
call %VENV_DIR%\Scripts\activate

rem Install requirements
if exist "requirements.txt" (
    echo Installing requirements...
    pip install -r requirements.txt
)

rem Run the GUI
echo Starting YouTube Playlist Downloader...
python gui.py
pause
