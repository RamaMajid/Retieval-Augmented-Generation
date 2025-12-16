@echo off
echo ========================================
echo Image Retrieval RAG - Backend Setup
echo ========================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/4] Installing dependencies (this may take a while)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Copying environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please edit it if needed
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file if needed (set DEVICE=cuda if you have GPU)
echo 2. Run: venv\Scripts\activate
echo 3. Run: python initialize.py (to load dataset)
echo 4. Run: python app.py (to start server)
echo.
pause
