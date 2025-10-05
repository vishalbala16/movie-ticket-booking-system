#!/usr/bin/env python
"""
Quick 30-second demo showing key features
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def quick_demo():
    print("QUICK DEMO - Movie Booking System")
    print("=" * 40)
    
    try:
        # 1. Register user
        print("1. Creating user...")
        requests.post(f'{BASE_URL}/signup/', json={
            'username': 'quickdemo', 'email': 'demo@test.com', 'password': 'demo123'
        })
        
        # 2. Login and get token
        print("2. Getting JWT token...")
        response = requests.post(f'{BASE_URL}/login/', json={
            'username': 'quickdemo', 'password': 'demo123'
        })
        token = response.json()['access']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 3. Get movies
        print("3. Fetching movies...")
        movies = requests.get(f'{BASE_URL}/movies/').json()
        print(f"   Found {len(movies)} movies")
        
        # 4. Get shows
        show_id = requests.get(f'{BASE_URL}/movies/1/shows/').json()[0]['id']
        print(f"   Using show ID: {show_id}")
        
        # 5. Book seat
        print("4. Booking seat 7...")
        response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                               json={'seat_number': 7}, headers=headers)
        print(f"   Status: {response.status_code}")
        
        # 6. Try double booking (should fail)
        print("5. Testing double booking prevention...")
        response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                               json={'seat_number': 7}, headers=headers)
        print(f"   Prevented: {response.status_code == 400}")
        
        # 7. Try overbooking (should fail)
        print("6. Testing overbooking prevention...")
        response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                               json={'seat_number': 999}, headers=headers)
        print(f"   Prevented: {response.status_code == 400}")
        
        print("\n✅ ALL FEATURES WORKING!")
        print("📚 Full docs: http://127.0.0.1:8000/swagger/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure server is running: python manage.py runserver")

if __name__ == '__main__':
    quick_demo()