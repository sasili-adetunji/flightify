from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    birth_date = models.DateField(
        null=True, blank=True,
        verbose_name='Date of birth')

    phone = models.CharField(
        max_length=50, null=True, blank=True,
        verbose_name='Phone')

    contact_address = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Address')

    contact_kin_name = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Name')

    contact_kin_relationship = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Relationship')

    contact_kin_phone = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Phone')

    contact_kin_mobile = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Mobile')

    contact_kin_email = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='E-mail')


    def get_full_name(self):
        """ Returns formatted users full name """
        return '{} {}'.format(self.first_name, self.last_name)
