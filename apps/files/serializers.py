from rest_framework import serializers
from apps.files.models import File


class FileSerializer(serializers.ModelSerializer):
    """ File serializer """

    uploader = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = File
        fields = '__all__'

    def get_uploader(self, file):
        return file.uploader.get_full_name()
