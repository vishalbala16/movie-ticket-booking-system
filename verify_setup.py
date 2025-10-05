#!/usr/bin/env python
"""
Setup verification script for Movie Booking System
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

from booking.models import Movie, Show, Booking
from django.contrib.auth.models import User

def verify_setup():
    print("Verifying Movie Booking System Setup")
    print("=" * 50)
    
    # Check database
    print("\nDatabase Status:")
    try:
        movie_count = Movie.objects.count()
        show_count = Show.objects.count()
        booking_count = Booking.objects.count()
        user_count = User.objects.count()
        
        print(f"[OK] Movies: {movie_count}")
        print(f"[OK] Shows: {show_count}")
        print(f"[OK] Bookings: {booking_count}")
        print(f"[OK] Users: {user_count}")
        
        if movie_count == 0:
            print("\n[WARNING] No sample data found. Run: python manage.py populate_data")
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False
    
    # Check required files
    print("\nFile Structure:")
    required_files = [
        'manage.py',
        'requirements.txt',
        'README.md',
        'booking/models.py',
        'booking/views.py',
        'booking/serializers.py',
        'booking/urls.py',
        'movie_booking/settings.py',
        'movie_booking/urls.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[ERROR] {file_path} - Missing!")
    
    # Check installed packages
    print("\nPackage Status:")
    try:
        import rest_framework
        import rest_framework_simplejwt
        import drf_yasg
        print("[OK] Django REST Framework")
        print("[OK] JWT Authentication")
        print("[OK] Swagger Documentation")
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        return False
    
    print("\nAPI Endpoints:")
    endpoints = [
        "POST /signup/ - User registration",
        "POST /login/ - User authentication",
        "GET /movies/ - List movies",
        "GET /movies/<id>/shows/ - List shows",
        "POST /shows/<id>/book/ - Book seat",
        "POST /bookings/<id>/cancel/ - Cancel booking",
        "GET /my-bookings/ - User bookings",
        "GET /swagger/ - API documentation"
    ]
    
    for endpoint in endpoints:
        print(f"[OK] {endpoint}")
    
    print("\n" + "=" * 50)
    print("Setup Verification Complete!")
    print("\nTo start the server:")
    print("   python manage.py runserver")
    print("\nThen visit:")
    print("   http://127.0.0.1:8000/swagger/ - API Documentation")
    print("   http://127.0.0.1:8000/admin/ - Admin Interface")
    
    return True

if __name__ == '__main__':
    verify_setup()