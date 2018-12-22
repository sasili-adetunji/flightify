from django.contrib.auth.models import AbstractUser
from django.db import models
# from apps.flight.models import Flight


class CustomUser(AbstractUser):

    birth_date = models.DateField(
        null=True, blank=True,
        verbose_name='Date of birth')

    phone = models.CharField(
        max_length=50, null=True, blank=True,
        verbose_name='Phone')

    passport_number = models.CharField(
        max_length=50, null=True, blank=True,
        verbose_name='Passport')

    contact_address = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Address')

    contact_kin_name = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='NOK Name')

    contact_kin_relationship = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Relationship')

    contact_kin_phone = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='NOK Phone')

    contact_kin_email = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='NOK E-mail')
    

    def get_full_name(self):
        """ Returns formatted users full name """
        return '{} {}'.format(self.first_name, self.last_name)
