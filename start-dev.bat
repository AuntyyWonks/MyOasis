@echo off
echo ========================================
echo    OASIS - Plant Assistant
echo    Professional Development Environment
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start cmd /k "cd oasis-serverside && echo Starting Flask Backend... && python app.py"

echo [2/2] Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo [2/2] Starting Frontend Development Server...
start cmd /k "cd client && echo Starting Vue Frontend... && npm run dev"

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