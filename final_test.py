#!/usr/bin/env python
"""
Final comprehensive test
"""
import os
import sys
import django
import subprocess
import time
import requests
from threading import Thread

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

def test_api_endpoints():
    """Test API endpoints"""
    base_url = 'http://127.0.0.1:8000'
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test movies endpoint
        response = requests.get(f'{base_url}/movies/', timeout=5)
        if response.status_code == 200:
            print("[OK] Movies endpoint working")
        else:
            print(f"[ERROR] Movies endpoint failed: {response.status_code}")
        
        # Test swagger endpoint
        response = requests.get(f'{base_url}/swagger/', timeout=5)
        if response.status_code == 200:
            print("[OK] Swagger documentation working")
        else:
            print(f"[ERROR] Swagger failed: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")

def run_server():
    """Run Django server"""
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '--noreload'])
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    print("Starting comprehensive test...")
    
    # Start server in background
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Test endpoints
    test_api_endpoints()
    
    print("Test completed. Server is ready!")
    print("\nTo start manually:")
    print("python manage.py runserver")
    print("\nThen visit:")
    print("http://127.0.0.1:8000/swagger/ - API Documentation")
    print("http://127.0.0.1:8000/movies/ - Movies API")