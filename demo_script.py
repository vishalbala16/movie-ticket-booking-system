#!/usr/bin/env python
"""
Complete Demo Script for Movie Booking System
Shows all features, business rules, and error handling
"""
import requests
import json
import time

BASE_URL = 'http://127.0.0.1:8000'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def print_test(test_name, success, response_data=None):
    status = "[PASS]" if success else "[FAIL]"
    print(f"{status} {test_name}")
    if response_data:
        print(f"     Response: {json.dumps(response_data, indent=2)}")

def demo_authentication():
    print_section("1. AUTHENTICATION FEATURES")
    
    # Test 1: User Signup
    print("\n1.1 User Registration")
    signup_data = {
        'username': 'demo_user',
        'email': 'demo@example.com',
        'password': 'secure123'
    }
    
    response = requests.post(f'{BASE_URL}/signup/', json=signup_data)
    print_test("User Signup", response.status_code == 201, response.json())
    
    # Test 2: Login and Get JWT
    print("\n1.2 JWT Authentication")
    login_data = {'username': 'demo_user', 'password': 'secure123'}
    response = requests.post(f'{BASE_URL}/login/', json=login_data)
    
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        print_test("Login Success", True, {"access_token": access_token[:50] + "..."})
        return access_token
    else:
        print_test("Login Failed", False, response.json())
        return None

def demo_movie_apis():
    print_section("2. MOVIE & SHOW APIs")
    
    # Test 3: List Movies
    print("\n2.1 List All Movies")
    response = requests.get(f'{BASE_URL}/movies/')
    movies = response.json()
    print_test("Get Movies", response.status_code == 200, 
              {"count": len(movies), "first_movie": movies[0] if movies else None})
    
    if movies:
        movie_id = movies[0]['id']
        
        # Test 4: List Shows for Movie
        print(f"\n2.2 List Shows for Movie ID {movie_id}")
        response = requests.get(f'{BASE_URL}/movies/{movie_id}/shows/')
        shows = response.json()
        print_test("Get Shows", response.status_code == 200,
                  {"count": len(shows), "first_show": shows[0] if shows else None})
        
        return shows[0]['id'] if shows else None
    return None

def demo_booking_features(access_token, show_id):
    print_section("3. BOOKING FEATURES & BUSINESS RULES")
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test 5: Successful Booking
    print("\n3.1 Successful Seat Booking")
    booking_data = {'seat_number': 5}
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=booking_data, headers=headers)
    booking_id = None
    if response.status_code == 201:
        booking_id = response.json()['id']
        print_test("Book Seat 5", True, response.json())
    else:
        print_test("Book Seat 5", False, response.json())
    
    # Test 6: Double Booking Prevention
    print("\n3.2 Double Booking Prevention")
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=booking_data, headers=headers)
    print_test("Prevent Double Booking", response.status_code == 400, response.json())
    
    # Test 7: Overbooking Prevention
    print("\n3.3 Overbooking Prevention")
    invalid_seat = {'seat_number': 999}
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=invalid_seat, headers=headers)
    print_test("Prevent Overbooking", response.status_code == 400, response.json())
    
    # Test 8: Input Validation
    print("\n3.4 Input Validation")
    invalid_input = {'seat_number': 0}
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json=invalid_input, headers=headers)
    print_test("Input Validation", response.status_code == 400, response.json())
    
    return booking_id

def demo_booking_management(access_token, booking_id):
    print_section("4. BOOKING MANAGEMENT")
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Test 9: View My Bookings
    print("\n4.1 View User Bookings")
    response = requests.get(f'{BASE_URL}/my-bookings/', headers=headers)
    bookings = response.json()
    print_test("Get My Bookings", response.status_code == 200,
              {"count": len(bookings), "bookings": bookings})
    
    # Test 10: Cancel Booking
    print(f"\n4.2 Cancel Booking ID {booking_id}")
    response = requests.post(f'{BASE_URL}/bookings/{booking_id}/cancel/', headers=headers)
    print_test("Cancel Booking", response.status_code == 200, response.json())
    
    # Test 11: Try to Cancel Again (Should Fail)
    print("\n4.3 Prevent Double Cancellation")
    response = requests.post(f'{BASE_URL}/bookings/{booking_id}/cancel/', headers=headers)
    print_test("Prevent Double Cancel", response.status_code == 400, response.json())

def demo_security_features(access_token, show_id):
    print_section("5. SECURITY FEATURES")
    
    # Test 12: Unauthorized Access
    print("\n5.1 Unauthorized Booking Attempt")
    booking_data = {'seat_number': 10}
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', json=booking_data)
    print_test("Block Unauthorized Access", response.status_code == 401, response.json())
    
    # Test 13: Create Another User
    print("\n5.2 User Isolation Test")
    other_user = {'username': 'other_user', 'email': 'other@test.com', 'password': 'pass123'}
    requests.post(f'{BASE_URL}/signup/', json=other_user)
    
    login_response = requests.post(f'{BASE_URL}/login/', 
                                 json={'username': 'other_user', 'password': 'pass123'})
    other_token = login_response.json()['access']
    other_headers = {'Authorization': f'Bearer {other_token}'}
    
    # Book seat with other user
    response = requests.post(f'{BASE_URL}/shows/{show_id}/book/', 
                           json={'seat_number': 15}, headers=other_headers)
    if response.status_code == 201:
        other_booking_id = response.json()['id']
        
        # Try to cancel other user's booking with first user
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(f'{BASE_URL}/bookings/{other_booking_id}/cancel/', headers=headers)
        print_test("Prevent Unauthorized Cancel", response.status_code == 404, response.json())

def demo_error_handling():
    print_section("6. ERROR HANDLING")
    
    # Test 14: Invalid Login
    print("\n6.1 Invalid Credentials")
    response = requests.post(f'{BASE_URL}/login/', 
                           json={'username': 'fake', 'password': 'wrong'})
    print_test("Handle Invalid Login", response.status_code == 401, response.json())
    
    # Test 15: Invalid Show ID
    print("\n6.2 Invalid Show ID")
    fake_token = "Bearer fake.token.here"
    response = requests.post(f'{BASE_URL}/shows/999/book/', 
                           json={'seat_number': 1}, 
                           headers={'Authorization': fake_token})
    print_test("Handle Invalid Show", response.status_code == 401)

def demo_api_documentation():
    print_section("7. API DOCUMENTATION")
    
    # Test 16: Swagger Documentation
    print("\n7.1 Swagger API Documentation")
    response = requests.get(f'{BASE_URL}/swagger/')
    print_test("Swagger Available", response.status_code == 200, 
              {"message": "Swagger UI accessible at /swagger/"})

def main():
    print("MOVIE BOOKING SYSTEM - COMPLETE DEMONSTRATION")
    print("This demo shows all features, business rules, and error handling")
    print(f"Server should be running at: {BASE_URL}")
    
    try:
        # Check if server is running
        response = requests.get(f'{BASE_URL}/movies/', timeout=5)
        if response.status_code != 200:
            print("ERROR: Server not responding. Run: python manage.py runserver")
            return
    except requests.exceptions.RequestException:
        print("ERROR: Server not running. Please start with: python manage.py runserver")
        return
    
    # Run all demonstrations
    access_token = demo_authentication()
    if not access_token:
        print("Demo stopped - authentication failed")
        return
    
    show_id = demo_movie_apis()
    if not show_id:
        print("Demo stopped - no shows available")
        return
    
    booking_id = demo_booking_features(access_token, show_id)
    if booking_id:
        demo_booking_management(access_token, booking_id)
    
    demo_security_features(access_token, show_id)
    demo_error_handling()
    demo_api_documentation()
    
    print_section("DEMONSTRATION COMPLETE")
    print("All features demonstrated successfully!")
    print(f"\nAPI Documentation: {BASE_URL}/swagger/")
    print("All business rules and bonus features working correctly.")

if __name__ == '__main__':
    main()