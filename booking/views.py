from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Movie, Show, Booking
from .serializers import UserSerializer, MovieSerializer, ShowSerializer, BookingSerializer, BookSeatSerializer

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: 'User created successfully'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={200: 'Login successful'}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

class MovieShowsView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

@swagger_auto_schema(
    method='post',
    request_body=BookSeatSerializer,
    responses={201: 'Seat booked successfully'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request, show_id):
    try:
        with transaction.atomic():
            show = get_object_or_404(Show, id=show_id)
            serializer = BookSeatSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            seat_number = serializer.validated_data['seat_number']
            
            # Validate seat number range
            if seat_number > show.total_seats:
                return Response(
                    {'error': f'Seat number must be between 1 and {show.total_seats}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if seat is already booked
            if Booking.objects.filter(show=show, seat_number=seat_number, status='booked').exists():
                return Response(
                    {'error': 'Seat already booked'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create booking
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seat_number=seat_number
            )
            
            return Response(
                BookingSerializer(booking).data, 
                status=status.HTTP_201_CREATED
            )
            
    except Exception as e:
        return Response(
            {'error': 'Booking failed. Please try again.'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@swagger_auto_schema(
    method='post',
    responses={200: 'Booking cancelled successfully'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        if booking.status == 'cancelled':
            return Response(
                {'error': 'Booking already cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({'message': 'Booking cancelled successfully'})
        
    except Booking.DoesNotExist:
        return Response(
            {'error': 'Booking not found or unauthorized'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')