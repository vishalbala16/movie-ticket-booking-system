from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', views.MovieShowsView.as_view(), name='movie-shows'),
    path('shows/<int:show_id>/book/', views.book_seat, name='book-seat'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),
]