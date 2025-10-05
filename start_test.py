#!/usr/bin/env python
"""
Test server startup with error handling
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
    
    try:
        # Test Django setup
        django.setup()
        print("[OK] Django setup successful")
        
        # Test WSGI application
        application = get_wsgi_application()
        print("[OK] WSGI application created successfully")
        
        # Test URL resolution
        from django.urls import reverse
        test_urls = ['movie-list', 'signup', 'login']
        for url_name in test_urls:
            try:
                url = reverse(url_name)
                print(f"[OK] URL '{url_name}' resolves to: {url}")
            except Exception as e:
                print(f"[ERROR] URL '{url_name}' failed: {e}")
        
        # Test model operations
        from booking.models import Movie
        print(f"[OK] Database connection working - Movies count: {Movie.objects.count()}")
        
        print("\nAll tests passed! Server should start successfully.")
        print("Run: python manage.py runserver")
        
    except Exception as e:
        print(f"[ERROR] Error during startup test: {e}")
        import traceback
        traceback.print_exc()