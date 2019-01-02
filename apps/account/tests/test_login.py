# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.account.models import CustomUser

User = get_user_model()

class LoginTest(APITestCase):

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

    def tearDown(self):
        self.user.delete()


class LoginTestExceptions(LoginTest):

    """
    Test class for login exceptions.
    """

    def test_login_username_empty(self):
        '''Login a User - Invalid :- When the username is empty'''
        data = self.data.copy()

        data['username'] = ''

        response = self.client.post(
            reverse('jwt_login'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_login_username_not_sent(self):
        '''Login a User - Invalid :- When the username not passed'''
        data = self.data.copy()
        data.pop('username')
        response = self.client.post(
            reverse('jwt_login'),
            data
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)

    def test_login_password_empty(self):
        '''Login a User - Invalid :- When the password is empty'''
        
        data = self.data.copy()
        data['password'] = ''
        response = self.client.post(
            reverse('jwt_login'),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_login_password_not_sent(self):
        '''Login a User - Invalid :- When the password not passed'''
        data = self.data.copy()
        data.pop('password')
        response = self.client.post(
            reverse('jwt_login'),
            data
        )

        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)

    def test_login_with_invalid_credentials(self):
        '''Login a User - Invalid :- When wrong username and passsword are passed'''
        data = self.data.copy()

        data['password'] = 'wrong'
        data['username'] = 'anotherwrong'

        response = self.client.post(
            reverse('jwt_login'),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Unable to log in because the username or password is invalid', status_code=400)


class LoginTestValid(LoginTest):
    """
    Test class for valid login.
    """

    def test_login_with_valid_credentials(self):
        '''
        Login a User - VALID :- When a valid username and password is used to login
        '''

        data = self.data.copy()
        response = self.client.post(
            reverse('jwt_login'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('message'),
            'User login Successfully.')
        self.assertContains(response, 'token', status_code=status.HTTP_200_OK)
        self.assertContains(response, 'user', status_code=status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('payload')['user']['username'],
            data['username']
        )

    def test_return_full_name_on_login(self):
        '''
        Login a User - VALID :- When a valid username and password return full name
        '''

        data = self.data.copy()
        response = self.client.post(
            reverse('jwt_login'),
            data
        )
        user = CustomUser.objects.get(pk=response.data.get('payload')['user']['id'])
        self.assertEqual(
            user.get_full_name(),
            'Test User'
        )