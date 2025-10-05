from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ShowSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Show
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='show.movie.title', read_only=True)
    screen_name = serializers.CharField(source='show.screen_name', read_only=True)
    show_datetime = serializers.DateTimeField(source='show.date_time', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class BookSeatSerializer(serializers.Serializer):
    seat_number = serializers.IntegerField(min_value=1)