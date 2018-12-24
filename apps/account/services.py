from datetime import datetime
from django.db import (
    transaction
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404 
from rest_framework import (
    exceptions
)
from apps.helpers.token import confirm_token
from apps.helpers.tasks import send_signup_email_task
from . import serializers as account_serializer

User = get_user_model()

def create_new_user(*, data):
    '''Creates a new user'''

    serializer = account_serializer.UserSerializer(
        data=data
    )

    with transaction.atomic():
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        send_signup_email_task.delay(data)

    return serializer.data


def confirm_user(*, key):
    '''Activates and confirm a new user'''

    assert isinstance(key, str)

    response = confirm_token(key)

    if response:
        user = get_object_or_404(User, email=response)
        if user.is_active == False:
            user.is_active = True
            user.save()
            return user

        # If user is already active, simply retun user
        else:
            return user

    # invalid token
    raise exceptions.APIException('invalid token')
