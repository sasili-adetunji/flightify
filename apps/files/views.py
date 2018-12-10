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
from . import serializers as file_serializers

from datetime import datetime
from . import (
    services as file_services
)
from apps.helpers.response import APIResponse


class UploadViewSet(viewsets.ViewSet):

    def create(self, request, **kwargs):
        ''' views to create a new file'''
        
        upload = file_services.upload_files(
            request.user,
            profile_pk=request.user.pk,
            description=request.data.get('description', ''),
            files=request.FILES,
        )
        return APIResponse(upload,
                status=status.HTTP_201_CREATED,
                message='Upload successfully uploaded.'
              )

    def list(self, request, **kwargs):
        ''' views to list files'''
  
        upload = file_services.list_files(
            request.user,
            profile_pk=request.user.pk
        )
        return APIResponse(upload,
                status=status.HTTP_200_OK,
                message='Upload successfully retrieved.'
              )

    def retrieve(self, request, pk):
        ''' views to retrieve a file'''
  
        file = file_services.retrieve_file(
            request.user,
            file_pk=pk
        )
        return APIResponse(file_serializers.FileSerializer(file).data,
                status=status.HTTP_200_OK,
                message='file successfully retrieved.'
              )

    def update(self, request, pk, **kwargs):
        ''' views to update a file'''
  
        file = file_services.update_file(
                request.user,
                profile_pk=request.user.pk,
                file_pk=pk,
                description=request.data.get('description', ''),
                files=request.FILES,
        )
        return APIResponse(file,
                status=status.HTTP_200_OK,
                message='file successfully updated.'
              )

    @decorators.action(detail=False, methods=['get'], url_path='download/(?P<key>.*)')
    def download_file(self, request, **kwargs):
        ''' views to dowwnload a file'''

        url = file_services.retrieve_file_url(
            request.user,
            file_key=kwargs.get('key', ''),
        )
        return APIResponse({'signed_url': url})
