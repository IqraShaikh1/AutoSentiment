@echo off
echo ==========================================
echo 🚀 Starting Product Comparison System
echo ==========================================
echo.

REM Check if trained model exists
if not exist "trained_model" (
    echo ❌ Trained model not found!
    echo 📝 Please run: python train_model.py first
    pause
    exit /b 1
)

echo ✅ Model found
echo.

REM Check dependencies
echo 📦 Checking dependencies...
python -c "import transformers, torch, flask, selenium" 2>nul
if errorlevel 1 (
    echo ❌ Missing dependencies!
    echo 📝 Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies OK
echo.

REM Ask user for mode
echo Choose mode:
echo 1^) Web Application ^(with UI^)
echo 2^) Command Line Interface
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo 🌐 Starting Web Application...
    echo.
    echo 📡 Backend: http://localhost:5000
    echo 🖥️  Frontend: http://localhost:8000
    echo.
    echo Press Ctrl+C to stop both servers
    echo.
    
    REM Start Flask in new window
    start "Flask Backend" cmd /k python app.py
    
    REM Wait for Flask to start
    timeout /t 3 /nobreak >nul
    
    REM Start HTTP server in new window
    start "Frontend Server" cmd /k python -m http.server 8000
    
    echo ✅ System started!
    echo.
    echo 👉 Open your browser to: http://localhost:8000
    echo.
    echo Close the server windows to stop the system
    pause
    
) else if "%choice%"=="2" (
    echo.
    echo 💻 Starting CLI mode...
    echo.
    python run_comparison.py
    pause
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)