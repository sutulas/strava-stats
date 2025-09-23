#!/usr/bin/env bash
# Build script for Render deployment

# Upgrade pip to latest version
pip install --upgrade pip

# Install dependencies with pre-compiled wheels when possible
pip install --only-binary=all -r requirements.txt

# If any packages fail with --only-binary=all, install them individually
# This is a fallback for packages that don't have wheels available
pip install numpy==1.24.4 --only-binary=all || pip install numpy==1.24.4
pip install pandas==2.0.3 --only-binary=all || pip install pandas==2.0.3
pip install matplotlib==3.7.5 --only-binary=all || pip install matplotlib==3.7.5

# Ensure uvicorn is properly installed and accessible
pip install uvicorn==0.35.0

# Verify uvicorn installation
python -c "import uvicorn; print('uvicorn installed successfully')"