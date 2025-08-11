#!/usr/bin/env python3
"""
Test script for the Strava Stats API
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoints"""
    print("Testing health endpoints...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health endpoint: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Data file exists: {data.get('data_file_exists')}")
        print(f"Workflow initialized: {data.get('workflow_initialized')}")

def test_data_overview():
    """Test data overview endpoint"""
    print("\nTesting data overview...")
    
    response = requests.get(f"{BASE_URL}/api/v1/data/overview")
    print(f"Data overview: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total activities: {data.get('total_activities')}")
        print(f"Activity types: {data.get('activity_types')}")

def test_examples():
    """Test examples endpoint"""
    print("\nTesting examples endpoint...")
    
    response = requests.get(f"{BASE_URL}/api/v1/examples")
    print(f"Examples: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Number of example categories: {len(data.get('examples', []))}")

def test_query(query, description):
    """Test a query endpoint"""
    print(f"\nTesting query: {description}")
    print(f"Query: {query}")
    
    payload = {
        "query": query,
        "include_chart": True
    }
    
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/api/v1/query",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    end_time = time.time()
    
    print(f"Status: {response.status_code}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Chart generated: {data.get('chart_generated')}")
        print(f"Response: {data.get('response')[:200]}...")
        
        # Test chart endpoint if chart was generated
        if data.get('chart_generated'):
            chart_response = requests.get(f"{BASE_URL}/api/v1/chart")
            print(f"Chart endpoint: {chart_response.status_code}")
            if chart_response.status_code == 200:
                print("Chart successfully retrieved")
    else:
        print(f"Error: {response.text}")

def main():
    """Run all tests"""
    print("Starting API tests...")
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    try:
        test_health()
        test_data_overview()
        test_examples()
        
        # Test some example queries
        test_queries = [
            ("What is my average running pace?", "Basic statistics"),
            ("How many miles have I run this year?", "Mileage query"),
            ("Create a chart showing my distance over time", "Chart generation")
        ]
        
        for query, description in test_queries:
            test_query(query, description)
            time.sleep(1)  # Small delay between requests
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 