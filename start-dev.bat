@echo off
echo ========================================
echo    OASIS - Plant Assistant
echo    Professional Development Environment
echo ========================================
echo.

:: -----------------------------
:: Step 1: Prepare Backend
:: -----------------------------
echo [1/3] Setting up Backend Virtual Environment...

cd oasis-serverside

:: Create venv if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate

:: Upgrade pip and install requirements
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Start Flask backend in a new terminal
echo Starting Flask Backend...
start cmd /k "call venv\Scripts\activate && python app.py"

cd ..

:: -----------------------------
:: Step 2: Start Frontend
:: -----------------------------
echo [2/3] Waiting for backend to initialize...

echo [3/3] Installing frontend dependencies and starting Dev Server...
cd client-react

:: Install dependencies if node_modules does not exist
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)

:: Start dev server in the same terminal
npm run dev

cd ..

echo.
echo ========================================
echo    SERVERS STARTING...
echo ========================================
echo Backend API: http://localhost:5000
echo Frontend UI: http://localhost:3000
echo.
echo Open your browser to http://localhost:3000
echo to access the Oasis interface.
echo.
echo Press any key to close this window...
pause > nul
