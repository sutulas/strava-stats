#!/usr/bin/env bash
# Build script for Render deployment

# Upgrade pip to latest version
pip install --upgrade pip

# Install dependencies without pandas first
pip install -r requirements-simple.txt

# Install numpy first (dependency for pandas)
pip install numpy==1.24.4

# Try to install pandas with wheels, fallback to source if needed
pip install pandas==2.0.3 --only-binary=all || pip install pandas==2.0.3

# Install matplotlib
pip install matplotlib==3.7.5

# Verify critical installations
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import uvicorn; print('uvicorn installed successfully')"
python -c "import pandas; print('pandas installed successfully')"