#!/usr/bin/env bash
# Start script for Render deployment

# Set the port from Render's PORT environment variable
export PORT=${PORT:-8000}

# Start the application
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT