from rest_framework import serializers
from apps.files.models import File


class FileSerializer(serializers.ModelSerializer):
    """ File serializer """

    class Meta:
        model = File
        fields = '__all__'
