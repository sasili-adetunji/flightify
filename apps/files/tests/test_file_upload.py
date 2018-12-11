# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.files.models import File
from unittest.mock import patch

from apps.files.services import MockS3Obj, MockStore
from apps.files import services as file_services
User = get_user_model()


mockstore = MockStore()

@patch(
    'apps.files.services.s3_presigned_url',
    new=mockstore.mock_presigned_url
)
@patch(
    'apps.files.services.s3_upload',
    new=mockstore.mock_upload
)
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


# class FileUploadTestExceptions(FileUploadTest):

#     """
#     Test class for login exceptions.
#     """

#     def test_login_username_empty(self):
#         '''Login a User - Invalid :- When the username is empty'''
#         data = self.data.copy()

#         data['username'] = ''

#         response = self.client.post(
#             reverse('jwt_login'),
#             data
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, 'blank', status_code=400)
#         self.assertContains(response, 'This field may not be blank.', status_code=400)

#     def test_login_username_not_sent(self):
#         '''Login a User - Invalid :- When the username not passed'''
#         data = self.data.copy()
#         data.pop('username')
#         response = self.client.post(
#             reverse('jwt_login'),
#             data
#         )
#         self.assertContains(response, 'required', status_code=400)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, 'This field is required.', status_code=400)

#     def test_login_password_empty(self):
#         '''Login a User - Invalid :- When the password is empty'''
        
#         data = self.data.copy()
#         data['password'] = ''
#         response = self.client.post(
#             reverse('jwt_login'),
#             data
#         )

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, 'blank', status_code=400)
#         self.assertContains(response, 'This field may not be blank.', status_code=400)

#     def test_login_password_not_sent(self):
#         '''Login a User - Invalid :- When the password not passed'''
#         data = self.data.copy()
#         data.pop('password')
#         response = self.client.post(
#             reverse('jwt_login'),
#             data
#         )

#         self.assertContains(response, 'required', status_code=400)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, 'This field is required.', status_code=400)

#     def test_login_with_invalid_credentials(self):
#         '''Login a User - Invalid :- When wrong username and passsword are passed'''
#         data = self.data.copy()

#         data['password'] = 'wrong'
#         data['username'] = 'anotherwrong'

#         response = self.client.post(
#             reverse('jwt_login'),
#             data
#         )

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertContains(response, 'Unable to log in because the username or password is invalid', status_code=400)


class FileUploadTestValid(FileUploadTest):
    """
    Test class for valid upload.
    """

    # def test_login_with_valid_credentials(self):
    #     '''
    #     Login a User - VALID :- When a valid username and password is used to login
    #     '''

    #     data = self.data.copy()
    #     response = self.client.post(
    #         reverse('jwt_login'),
    #         data
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(
    #         response.data.get('message'),
    #         'User login Successfully.')
    #     self.assertContains(response, 'token', status_code=status.HTTP_200_OK)
    #     self.assertContains(response, 'user', status_code=status.HTTP_200_OK)
    #     self.assertEqual(
    #         response.data.get('payload')['user']['username'],
    #         data['username']
    #     )

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

    def test_retrieve_file(self):
        retrieved_file = file_services.retrieve_file(
            self.users,
            self.file_instance.id
        )
        self.assertEqual(self.file_instance, retrieved_file)