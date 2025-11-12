@echo off
echo ========================================
echo Link Planning GUI - Starting
echo ========================================
echo.

cd /d C:\Users\robin\PycharmProjects\linkdb

echo Checking Flask installation...
.venv\Scripts\python.exe -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Flask not found. Installing...
    .venv\Scripts\python.exe -m pip install flask
)

echo.
echo Starting GUI server...
echo.
echo ========================================
echo GUI will open in your browser at:
echo http://127.0.0.1:5000
echo ========================================
echo.
echo Press CTRL+C to stop the server
echo.

start http://127.0.0.1:5000
.venv\Scripts\python.exe gui_app.py

