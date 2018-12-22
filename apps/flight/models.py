from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Flight(models.Model):
    """ Flight model definition """

    ONE_WAY = 0
    ROUND_TRIP = 1

    FARE_CHOICES = (
        (ONE_WAY, 'One-Way'),
        (ROUND_TRIP, 'Round-Trip'),
    )

    passenger = models.ForeignKey(
        User,
        related_name="passenger",
        on_delete=models.PROTECT
    )

    depart_date = models.DateTimeField(
        verbose_name='Depart Date')

    return_date = models.DateTimeField(
        verbose_name='Return Date')

    departure = models.CharField(
        max_length=100,
        verbose_name='Departure')

    destination = models.CharField(
        max_length=100,
        verbose_name='Destination')

    fare = models.IntegerField(
        choices=FARE_CHOICES,
        verbose_name='Fare')


    booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
