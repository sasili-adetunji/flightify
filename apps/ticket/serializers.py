from rest_framework import serializers
from apps.flight.serializers import FlightSerializer
from django.contrib.auth import get_user_model
from rest_framework import (
    serializers,
    validators
)
from apps.account.serializers import UserSerializer
from apps.ticket.models import Passenger
User = get_user_model()

class BookTicketSerializer(serializers.ModelSerializer):

    user_email = serializers.SerializerMethodField(
        read_only=True
    )
  
    username = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Passenger
        fields = '__all__'

    def get_user_email(self, passenger):
        return passenger.flight.passenger.email

    def get_username(self, passenger):
        return passenger.flight.passenger.username

class BookFlightTicketSerializer(serializers.ModelSerializer):
  
    ticket = BookTicketSerializer()

    class Meta:
        model = Passenger
        fields = '__all__'

