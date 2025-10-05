#!/usr/bin/env python
"""
Simple API test script to verify all endpoints work correctly.
Run this after starting the Django server with: python manage.py runserver
"""

import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_api():
    print("🎬 Testing Movie Booking API")
    print("=" * 50)
    
    # Test 1: Signup
    print("\n1. Testing Signup...")
    signup_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/signup/', json=signup_data)
        if response.status_code == 201:
            print("✅ Signup successful")
        else:
            print(f"❌ Signup failed: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start with: python manage.py runserver")
        return
    
    # Test 2: Login
    print("\n2. Testing Login...")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/login/', json=login_data)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        print("✅ Login successful")
        print(f"Access Token: {access_token[:50]}...")
    else:
        print(f"❌ Login failed: {response.text}")
        return
    
    # Headers for authenticated requests
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test 3: List Movies
    print("\n3. Testing Movie List...")
    response = requests.get(f'{BASE_URL}/movies/')
    if response.status_code == 200:
        movies = response.json()
        print(f"✅ Found {len(movies)} movies")
        if movies:
            movie_id = movies[0]['id']
            print(f"First movie: {movies[0]['title']}")
        else:
            print("No movies found. Run: python manage.py populate_data")
            return
    else:
        print(f"❌ Failed to get movies: {response.text}")
        return
    
    # Test 4: List Shows for Movie
    print(f"\n4. Testing Shows for Movie ID {movie_id}...")
    response = requests.get(f'{BASE_URL}/movies/{movie_id}/shows/')
    if response.status_code == 200:
        shows = response.json()
        print(f"✅ Found {len(shows)} shows")
        if shows:
            show_id = shows[0]['id']
            print(f"First show: {shows[0]['screen_name']} at {shows[0]['date_time']}")
        else:
            print("No shows found")
            return
    else:
        print(f"❌ Failed to get shows: {response.text}")
        return
    
    # Test 5: Book a Seat
    print(f"\n5. Testing Seat Booking for Show ID {show_id}...")
    booking_data = {'seat_number': 5}
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=booking_data, headers=headers)
    if response.status_code == 201:
        booking = response.json()
        booking_id = booking['id']
        print(f"✅ Seat {booking['seat_number']} booked successfully")
    else:
        print(f"❌ Booking failed: {response.text}")
        return
    
    # Test 6: List My Bookings
    print("\n6. Testing My Bookings...")
    response = requests.get(f'{BASE_URL}/my-bookings/', headers=headers)
    if response.status_code == 200:
        bookings = response.json()
        print(f"✅ Found {len(bookings)} bookings")
    else:
        print(f"❌ Failed to get bookings: {response.text}")
    
    # Test 7: Cancel Booking
    print(f"\n7. Testing Booking Cancellation for Booking ID {booking_id}...")
    response = requests.post(f'{BASE_URL}/bookings/{booking_id}/cancel/', 
                           headers=headers)
    if response.status_code == 200:
        print("✅ Booking cancelled successfully")
    else:
        print(f"❌ Cancellation failed: {response.text}")
    
    # Test 8: Try Double Booking (should fail)
    print(f"\n8. Testing Double Booking Prevention...")
    booking_data = {'seat_number': 1}
    # First booking
    requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                 json=booking_data, headers=headers)
    # Second booking (should fail)
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=booking_data, headers=headers)
    if response.status_code == 400:
        print("✅ Double booking prevented successfully")
    else:
        print(f"❌ Double booking not prevented: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print(f"📚 View API docs at: {BASE_URL}/swagger/")

if __name__ == '__main__':
    test_api()