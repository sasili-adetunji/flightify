from django.db import (
    transaction
)

from . import serializers as account_serializer
from apps.helpers.token import generate_confirmation_token, confirm_token
from datetime import datetime
from django.shortcuts import get_object_or_404 
from rest_framework import (
    exceptions
)
from apps.helpers.email_helper import send_signup_confirmation
from apps.helpers.tasks import send_signup_email_task
from django.contrib.auth import get_user_model
User = get_user_model()

def create_new_user(*, data):
    '''Creates a new user'''
    serializer = account_serializer.UserSerializer(
        data=data
    )
    with transaction.atomic():
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        # send_signup_confirmation(data)
        send_signup_email_task.delay(data)
    return serializer.data


def confirm_user(*, key):

    assert isinstance(key, str)

    response = confirm_token(key)
    if response:
        user = get_object_or_404(User, email=response)
        if user.is_active == False:
            user.is_active = True
            user.save()
            return user

        #If user is already active, simply retun user
        else:
            return user

    # invalid token
    # raise 
    return 'Not valid'
