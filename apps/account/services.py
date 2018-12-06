from django.db import (
    transaction
)

from . import serializers as account_serializer
# from apps.helpers.token import generate_confirmation_token, confirm_token
# from datetime import datetime
# from django.shortcuts import get_object_or_404 
# from django.contrib.auth.models import User
# from rest_framework import (
#     exceptions
# )


def create_new_user(*, data):
    '''Creates a new user'''
    serializer = account_serializer.UserSerializer(
        data=data
    )
    with transaction.atomic():
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    return serializer.data


# def confirm_user(*, key):

#     assert isinstance(key, str)

#     response = confirm_token(key)
#     import pdb; pdb.set_trace()

#     if response is not False:
#         user = User.objects.get(email=response)
#         if user.is_active == False:
#             user.is_active = True
#             user.save()

#         #If user is already active, simply display error message
#         else:
#             raise exceptions.
#             already_active = True #Display : error message
#     raise
