from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()



class Ticket(models.Model):
    """ Ticket model definition """

    description = models.TextField(
        null=True, blank=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
