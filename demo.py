#!/usr/bin/env python
"""
Simple demo script for Movie Booking System
"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def demo():
    print("Movie Booking System Demo")
    print("=" * 30)
    
    try:
        # Register user
        print("1. Creating user...")
        requests.post(f'{BASE_URL}/signup/', json={
            'username': 'demo', 'email': 'demo@test.com', 'password': 'demo123'
        })
        
        # Login
        print("2. Getting JWT token...")
        response = requests.post(f'{BASE_URL}/login/', json={
            'username': 'demo', 'password': 'demo123'
        })
        token = response.json()['access']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get movies and book seat
        movies = requests.get(f'{BASE_URL}/movies/').json()
        show_id = requests.get(f'{BASE_URL}/movies/1/shows/').json()[0]['id']
        
        print("3. Booking seat...")
        response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                               json={'seat_number': 5}, headers=headers)
        print(f"   Booking: {'Success' if response.status_code == 201 else 'Failed'}")
        
        # Test double booking prevention
        print("4. Testing double booking prevention...")
        response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                               json={'seat_number': 5}, headers=headers)
        print(f"   Prevention: {'Working' if response.status_code == 400 else 'Failed'}")
        
        print("\nDemo complete! Visit http://127.0.0.1:8000/swagger/ for API docs")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure server is running: python manage.py runserver")

if __name__ == '__main__':
    demo()