from django.db import (
    transaction
)
from . import serializers as flight_serializer
from django.contrib.auth import get_user_model
from apps.flight.models import Flight
from rest_framework.exceptions import APIException
import pytz

from datetime import datetime, timedelta
from apps.account.serializers import UsersSerializer
User = get_user_model()

def create_flight(requestor, data):
    '''Creates a new flight'''
    # import pdb; pdb.set_trace()
    flight_info = data.copy()
    flight_info['passenger'] = requestor.id
    serializer = flight_serializer.FlightSerializer(
  
      data=flight_info
    )
    with transaction.atomic():
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return serializer.data

def list_flights(requestor, profile_pk):

    result = []

    flights = Flight.objects.filter(
        passenger=profile_pk
    )
    for flight in flights:
        result.append({
            'flight': flight_serializer.FlightSerializer(flight).data,
        })

    return result

def retrieve_flight(requestor, flight_pk):

    flight = Flight.objects.get(pk=flight_pk)
    return {
      'flight': flight_serializer.FlightSerializer(flight).data,
    }

def update_flight(requestor, flight_pk, data):

    flight_info = data.copy()
    flight = Flight.objects.get(pk=flight_pk)
    updated_flight = flight_serializer.FlightSerializer(
        data=flight_info,
        instance=flight,
        partial=True
    )

    with transaction.atomic():
        if updated_flight.is_valid(raise_exception=True):
            updated_flight.save()

    return updated_flight.data

def list_users(requestor, day):
    ''' List users for a flight in a given day'''

    date_ = day.split('-')

    try:
        year = int(date_[0])
        month = int(date_[1])
        day = int(date_[2])
        today = datetime(year=year, month=month, day=day, hour=0, minute=0, second=0).replace(tzinfo=pytz.UTC)
    except:
        raise APIException(detail='Provide proper date')

    flights = Flight.objects.filter(
        depart_date__gte=today, depart_date__lt=today+timedelta(hours=24)
        )
    
    total_users = flights.count()

    flight_users = []

    for flight in flights:
        flight_users.append(flight.passenger)

    return {
        "users":  UsersSerializer(flight_users, many=True).data,
        "users_count": total_users
        }
