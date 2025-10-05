@echo off
echo Starting Movie Booking System...
echo.

echo Checking if sample data exists...
python manage.py shell -c "from booking.models import Movie; print(f'Movies in database: {Movie.objects.count()}')"

echo.
echo Starting Django development server...
echo API will be available at: http://127.0.0.1:8000/
echo Swagger docs at: http://127.0.0.1:8000/swagger/
echo.

python manage.py runserver