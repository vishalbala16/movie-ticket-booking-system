from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Show, Booking
from django.utils import timezone

class BookingLogicTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.movie = Movie.objects.create(title='Test Movie', duration_minutes=120)
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name='Test Screen',
            date_time=timezone.now(),
            total_seats=10
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_successful_booking(self):
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_double_booking_prevention(self):
        # First booking
        Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        
        # Try to book same seat
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already booked', response.data['error'])

    def test_overbooking_prevention(self):
        url = reverse('book-seat', kwargs={'show_id': self.show.id})
        data = {'seat_number': 15}  # Exceeds total_seats (10)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking(self):
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=1)
        url = reverse('cancel-booking', kwargs={'booking_id': booking.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_unauthorized_cancel(self):
        other_user = User.objects.create_user(username='other', password='pass')
        booking = Booking.objects.create(user=other_user, show=self.show, seat_number=1)
        url = reverse('cancel-booking', kwargs={'booking_id': booking.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)