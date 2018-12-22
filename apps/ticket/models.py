from django.db import models
from apps.flight.models import Flight


class Passenger(models.Model):

    flight = models.ForeignKey(
        Flight,
        related_name="flight",
        on_delete=models.PROTECT
    )

    birth_date = models.DateField(
        verbose_name='Date of birth')

    phone = models.CharField(
        max_length=50,
        verbose_name='Phone')

    passport_number = models.CharField(
        max_length=50,
        verbose_name='Passport')

    contact_address = models.CharField(
        max_length=255,
        verbose_name='Address')

    contact_kin_name = models.CharField(
        max_length=255,
        verbose_name='NOK Name')

    contact_kin_relationship = models.CharField(
        max_length=255,
        verbose_name='Relationship')

    contact_kin_phone = models.CharField(
        max_length=255,
        verbose_name='NOK Phone')

    contact_kin_email = models.CharField(
        max_length=255,
        verbose_name='NOK E-mail')

