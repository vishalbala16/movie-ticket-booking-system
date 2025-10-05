import subprocess
import time
import requests
import threading
import sys

def start_server():
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8002', '--noreload'], 
                      timeout=15, capture_output=True)
    except subprocess.TimeoutExpired:
        pass

def test_endpoints():
    time.sleep(3)
    
    try:
        # Test movies endpoint
        response = requests.get('http://127.0.0.1:8002/movies/', timeout=5)
        movies_ok = response.status_code == 200
        
        # Test swagger
        response = requests.get('http://127.0.0.1:8002/swagger/', timeout=5)
        swagger_ok = response.status_code == 200
        
        # Test signup
        signup_data = {'username': 'testuser123', 'email': 'test@test.com', 'password': 'testpass123'}
        response = requests.post('http://127.0.0.1:8002/signup/', json=signup_data, timeout=5)
        signup_ok = response.status_code == 201
        
        print(f"Movies API: {'OK' if movies_ok else 'FAIL'}")
        print(f"Swagger: {'OK' if swagger_ok else 'FAIL'}")
        print(f"Signup: {'OK' if signup_ok else 'FAIL'}")
        
        return movies_ok and swagger_ok and signup_ok
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    print("Testing Movie Booking System...")
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    success = test_endpoints()
    
    if success:
        print("\nPROJECT IS READY!")
        print("All endpoints working correctly.")
        print("Run: python manage.py runserver")
        print("Visit: http://127.0.0.1:8000/swagger/")
    else:
        print("\nIssues found - check configuration")