# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.files.models import File
from unittest.mock import patch
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework_jwt import utils
import time

from apps.files import services as file_services
User = get_user_model()

def generate_token(user):
    assert(isinstance(user, User))
    token = utils.jwt_encode_handler(
        utils.jwt_payload_handler(user)
    )

    return '{0} {1}'.format(settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'], token)


@patch('apps.files.services.s3_presigned_url')
@patch('apps.files.services.s3_upload')
@patch('apps.files.services.s3_delete')
class FileUploadTest(APITestCase):

    """
    Base class for testing Login.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email='testuser@example.com', password='samplepassowrd',
            username='tester',
            first_name='Test',
            last_name='User'
        )
        self.data = {
            'username': 'tester',
            'password': 'samplepassowrd'
        }

        self.file_instance = self._create_file_instance(
            name='random_file',
            file_type='text/plain',
            uploader=self.user
        )

        fake_file = BytesIO(b'fakefiledata')
        fake_file.name = 'fake_file.jpg'
        file_upload = SimpleUploadedFile('file.txt', b'content')

        self.data = {
            'description': 'a random description',
            'files': file_upload,
        }

        self.file = self.client.post(
            reverse(
                'uploads-list',
            ),
            data=self.data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )

    # def tearDown(self):
    #     self.user.delete()

    def _create_file_instance(self, name, file_type, uploader, **kwargs):
        created_file = File.objects.create(
            name=name,
            type=file_type,
            uploader=uploader,
            **kwargs
        )
        file_key = 'user/{}/{}/{}'.format(
            self.user.id,
            created_file.id,
            created_file.name
        )
        created_file.s3_key = file_key
        created_file.save()
        return created_file

class FileUploadTestValid(FileUploadTest):
    """
    Test class for valid upload.
    """

    def test_make_file_key(self):
        obtained_key = file_services.make_file_key(
            self.user.id,
            self.file_instance.name,
            self.file_instance.id
        )
        expected_key = (
            'user/{}/{}/{}'.format(
                self.user.id,
                self.file_instance.id,
                self.file_instance.name
            )
        )

        self.assertEqual(expected_key, obtained_key)

    def test_create_upload(self):
        response = self.client.post(
            reverse(
                'uploads-list',
            ),
            data=self.data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('message'), 'File successfully uploaded.')

    def test_list_file(self):
  
        response = self.client.get(
            reverse(
                'uploads-list',
            ),
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Upload successfully retrieved.')
        self.assertEqual(response.data.get('payload')[0]['file']['uploader_name'], 'Test User')
        self.assertEqual(response.data.get('payload')[0]['file']['uploader_name'], 'Test User')

    def test_retrieve_file(self):

        response = self.client.get(
            reverse(
                'uploads-detail', args=[self.file_instance.id]
            ),
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'File successfully retrieved.')
        self.assertEqual(response.data.get('payload')['file']['uploader_name'], 'Test User')


    def test_update_file(self):

        new_data = self.data.copy()
        new_data['description'] = 'a new description'

        response = self.client.put(
            reverse(
                'uploads-detail', args=[self.file_instance.id]
            ),
            data=new_data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'file successfully updated.')
        self.assertEqual(response.data.get('payload')['description'], 'a new description')

    def test_delete_file(self):

        new_data = self.data.copy()
        new_data['description'] = 'a new description'

        response = self.client.delete(
            reverse(
                'uploads-detail', args=[self.file_instance.id]
            ),
            data=new_data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data.get('message'), 'file successfully deleted.')
        self.assertEqual(File.objects.filter(pk=self.file_instance.id).count(), 0)
