#!/usr/bin/env python3
"""
Test script for the data refresh functionality
This script tests the backend endpoints without going through the full OAuth flow
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"
TEST_TOKEN = "test_token"  # This would be a real token in production

def test_data_status():
    """Test the data status endpoint"""
    print("Testing data status endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/data/status")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Data Status Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing data status: {e}")

def test_data_refresh():
    """Test the data refresh endpoint"""
    print("\nTesting data refresh endpoint...")
    
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/data/refresh", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Data Refresh Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing data refresh: {e}")

def test_health_check():
    """Test the health check endpoint"""
    print("\nTesting health check endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Health Check Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing health check: {e}")

def check_files():
    """Check if the data files exist"""
    print("\nChecking data files...")
    
    files_to_check = [
        "data/formatted_data.csv",
        "fixed_formatted_run_data.csv"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} exists ({size} bytes)")
        else:
            print(f"✗ {file_path} does not exist")

if __name__ == "__main__":
    print("Testing Strava Data Refresh Backend")
    print("=" * 40)
    
    # Test basic endpoints
    test_health_check()
    test_data_status()
    
    # Test data refresh (will likely fail without real token)
    test_data_refresh()
    
    # Check file status
    check_files()
    
    print("\nTest completed!") 