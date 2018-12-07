import re
from rest_framework import (
    serializers,
    validators
)
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer
)
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

FAILED_LOGIN_MESSAGE = _('Unable to log in because the username or password is invalid')

class CustomJSONWebTokenSerializer(JSONWebTokenSerializer):

    ''' validates and authenticate users on login '''

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                raise serializers.ValidationError(FAILED_LOGIN_MESSAGE)
        else:
            raise serializers.ValidationError(FAILED_LOGIN_MESSAGE)


class UserSerializer(serializers.ModelSerializer):

    ''' serializes and validates user's data '''
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True,
    )
    last_name = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
        required=True
    )
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
        )

    def validate_username(self, username):
        '''Validate username '''
        if re.search(r'([^a-zA-Z/._\d+])', username) is None:
            return username
        raise serializers.ValidationError(
            'Username can only contain alphanumeric characters and . or _.'
        )

    def validate_password(self, password):
        '''Validate password'''
        if re.search(r'(^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$_!%*?&]{8,}$)', password) is not None:
            return password
        raise serializers.ValidationError(
            'Must have at least 1 uppercase, 1 lowercase, 1 number & 1 special character and 8 characters minimum'
        )

    def create(self, validated_data):
        '''creates a user '''

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
