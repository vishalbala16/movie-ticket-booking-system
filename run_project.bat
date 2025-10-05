@echo off
echo ========================================
echo Movie Ticket Booking System
echo ========================================
echo.

echo Checking system...
python start_test.py

echo.
echo Starting Django server...
echo.
echo API Documentation: http://127.0.0.1:8000/swagger/
echo Movies API: http://127.0.0.1:8000/movies/
echo Admin Panel: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver