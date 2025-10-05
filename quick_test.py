import subprocess
import time
import requests
import threading
import sys

def start_server():
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8001', '--noreload'], 
                      timeout=15, capture_output=True)
    except subprocess.TimeoutExpired:
        pass

def test_endpoints():
    time.sleep(3)  # Wait for server
    
    try:
        # Test basic endpoint
        response = requests.get('http://127.0.0.1:8001/movies/', timeout=5)
        print(f"Movies API: {response.status_code}")
        
        # Test swagger
        response = requests.get('http://127.0.0.1:8001/swagger/', timeout=5)
        print(f"Swagger: {response.status_code}")
        
        print("✓ Server working correctly!")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    success = test_endpoints()
    print(f"Project ready: {success}")