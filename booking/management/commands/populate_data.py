from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from booking.models import Movie, Show

class Command(BaseCommand):
    help = 'Populate database with sample movies and shows'

    def handle(self, *args, **options):
        # Create sample movies
        movies_data = [
            {'title': 'Avengers: Endgame', 'duration_minutes': 181},
            {'title': 'Spider-Man: No Way Home', 'duration_minutes': 148},
            {'title': 'The Dark Knight', 'duration_minutes': 152},
            {'title': 'Inception', 'duration_minutes': 148},
            {'title': 'Interstellar', 'duration_minutes': 169},
        ]
        
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(**movie_data)
            if created:
                self.stdout.write(f'Created movie: {movie.title}')
        
        # Create sample shows
        movies = Movie.objects.all()
        screens = ['Screen A', 'Screen B', 'Screen C']
        
        for movie in movies:
            for i, screen in enumerate(screens):
                show_time = timezone.now() + timedelta(days=i+1, hours=i*3)
                show, created = Show.objects.get_or_create(
                    movie=movie,
                    screen_name=screen,
                    date_time=show_time,
                    defaults={'total_seats': 100}
                )
                if created:
                    self.stdout.write(f'Created show: {show}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))