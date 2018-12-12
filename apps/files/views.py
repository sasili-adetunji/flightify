from rest_framework import (
    viewsets,
    status
)
from . import serializers as file_serializers
from . import (
    services as file_services
)
from apps.helpers.response import APIResponse


class UploadViewSet(viewsets.ViewSet):

    def create(self, request):
        ''' views to create a new file'''
        
        file = file_services.upload_files(
            request.user,
            profile_pk=request.user.pk,
            description=request.data.get('description', ''),
            files=request.FILES,
        )
        return APIResponse(file,
                status=status.HTTP_201_CREATED,
                message='File successfully uploaded.'
              )

    def list(self, request):
        ''' views to list files'''
  
        file = file_services.list_files(
            request.user,
            profile_pk=request.user.pk
        )
        return APIResponse(file,
                status=status.HTTP_200_OK,
                message='Upload successfully retrieved.'
              )

    def retrieve(self, request, pk):
        ''' views to retrieve a file'''
  
        file = file_services.retrieve_file(
            request.user,
            file_pk=pk
        )
        return APIResponse(file,
                status=status.HTTP_200_OK,
                message='File successfully retrieved.'
              )

    def update(self, request, pk):
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

    def destroy(self, request, pk):
        ''' views to delete a file'''

        file = file_services.delete_file(
                request.user,
                profile_pk=request.user.pk,
                file_pk=pk,
        )
        return APIResponse(file,
                status=status.HTTP_204_NO_CONTENT,
                message='file successfully deleted.'
              )
