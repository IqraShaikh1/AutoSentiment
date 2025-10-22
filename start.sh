#!/bin/bash

echo "=========================================="
echo "🚀 Starting Product Comparison System"
echo "=========================================="
echo ""

# Check if trained model exists
if [ ! -d "trained_model" ]; then
    echo "❌ Trained model not found!"
    echo "📝 Please run: python train_model.py first"
    exit 1
fi

echo "✅ Model found"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python -c "import transformers, torch, flask, selenium" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies!"
    echo "📝 Installing requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo "✅ Dependencies OK"
echo ""

# Ask user for mode
echo "Choose mode:"
echo "1) Web Application (with UI)"
echo "2) Command Line Interface"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "🌐 Starting Web Application..."
    echo ""
    echo "📡 Backend: http://localhost:5000"
    echo "🖥️  Frontend: http://localhost:8000"
    echo ""
    echo "Press Ctrl+C to stop"
    echo ""
    
    # Start Flask in background
    python app.py &
    FLASK_PID=$!
    
    # Wait for Flask to start
    sleep 3
    
    # Start simple HTTP server for frontend
    python -m http.server 8000 &
    HTTP_PID=$!
    
    echo "✅ System started!"
    echo ""
    echo "👉 Open your browser to: http://localhost:8000"
    echo ""
    
    # Wait for user to stop
    read -p "Press Enter to stop the system..."
    
    # Kill processes
    kill $FLASK_PID $HTTP_PID 2>/dev/null
    echo ""
    echo "👋 System stopped"
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "💻 Starting CLI mode..."
    echo ""
    python run_comparison.py
else
    echo "❌ Invalid choice"
    exit 1
fi