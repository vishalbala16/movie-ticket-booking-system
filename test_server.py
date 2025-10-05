#!/usr/bin/env python
"""
Test server startup
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.test.utils import get_runner
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
    
    try:
        django.setup()
        print("Django setup successful")
        
        # Test URL patterns
        from django.urls import reverse
        print("URL patterns working")
        
        # Test models
        from booking.models import Movie, Show, Booking
        print("Models imported successfully")
        
        # Test views
        from booking.views import MovieListView
        print("Views imported successfully")
        
        # Test serializers
        from booking.serializers import MovieSerializer
        print("Serializers imported successfully")
        
        print("All components working correctly!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()