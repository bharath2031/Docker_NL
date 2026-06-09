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

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running on localhost:11434"
    echo "   Please start Ollama with: ollama serve"
    echo "   Or use Docker Compose to start all services"
    read -p "   Continue anyway? (y/N): " choice
    if [[ ! $choice =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Ollama is running"
    
    # Check if llama3 model is available
    if ! curl -s http://localhost:11434/api/tags | grep -q "llama3"; then
        echo "⚠️  llama3 model not found"
        read -p "   Do you want to pull it now? (y/N): " choice
        if [[ $choice =~ ^[Yy]$ ]]; then
            echo "   Pulling llama3 model (this may take a few minutes)..."
            ollama pull llama3
        fi
    else
        echo "✅ llama3 model is available"
    fi
fi

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
