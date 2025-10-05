#!/usr/bin/env python
"""
Test Swagger configuration
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking.settings')
django.setup()

try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from rest_framework import permissions
    
    schema_view = get_schema_view(
       openapi.Info(
          title="Movie Ticket Booking API",
          default_version='v1',
          description="A comprehensive movie ticket booking system with JWT authentication",
          contact=openapi.Contact(email="contact@moviebooking.local"),
          license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
    )
    
    print("Swagger configuration successful!")
    
except Exception as e:
    print(f"Swagger error: {e}")
    import traceback
    traceback.print_exc()