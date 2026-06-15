#!/bin/bash

# Startup script for AI Docker NL Dashboard

echo "========================================"
echo "AI Docker NL Dashboard - Startup Script"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi
echo "✅ Docker is running"


# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data logs prompts

# Check if Python dependencies are installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo ""
    echo "⚠️  Python dependencies not found"
    read -p "   Install dependencies now? (y/N): " choice
    if [[ $choice =~ ^[Yy]$ ]]; then
        echo "   Installing dependencies..."
        pip install -r requirements.txt
    else
        echo "   Please install dependencies with: pip install -r requirements.txt"
        exit 1
    fi
else
    echo "✅ Python dependencies installed"
fi

# Start the application
echo ""
echo "========================================"
echo "Starting Dashboard..."
echo "========================================"
echo ""
echo "Dashboard will be available at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run app.py
