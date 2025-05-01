
@echo off
REM Create virtual environment
python -m venv venv

REM Activate virtual environment and install dependencies
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete. To run the app, double-click run_app.bat
pause
