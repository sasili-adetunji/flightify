from apps.account.serializers import CustomJSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from apps.helpers.utils import jwt_response_payload_handler
from rest_framework import (
    viewsets,
    exceptions,
    decorators,
    status
)
from datetime import datetime
from . import (
    services as accounts_services
)
from apps.helpers.response import APIResponse


class UserViewSet(viewsets.ViewSet):

    permission_classes = (AllowAny,)

    @decorators.action(detail=False, methods=['post'], url_path='signup')
    def create_user(self, request, **kwargs):
        ''' views to create a new user'''
        return APIResponse(
            accounts_services.create_new_user(data=request.data),
            status=status.HTTP_201_CREATED,
            message='User Account Created Successfully.'
        )


class JWTLogin(JSONWebTokenAPIView):

    serializer_class = CustomJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        ''' views to login a user'''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            return APIResponse(jwt_response_payload_handler(token, user, request),
                status=status.HTTP_200_OK,
                message='User login Successfully.'
            )

        raise exceptions.AuthenticationFailed(detail=serializer.errors)
