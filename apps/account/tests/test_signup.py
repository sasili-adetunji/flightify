# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch, ANY
from apps.helpers.token import generate_confirmation_token, confirm_token
from django.core.mail import send_mail

User = get_user_model()

class SignupTest(APITestCase):

    """
    Base class for testing Signup.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email='testuser@example.com', password='samplePassword@2',
            username='tester',
            first_name='Test',
            last_name='User'
        )
        self.data = {
            'username': 'tester2',
            'password': 'Samplepassowrd2@',
            'email': 'tester1@gmail.com',
            'first_name': 'Test2',
            'last_name': 'User2'
        }

    def tearDown(self):
        self.user.delete()


class SignupTestExceptions(SignupTest):

    """
    Test class for signup exceptions.
    """
  
    def test_signup_with_username_empty(self):
        '''Signup a User - Invalid :- When the username is empty'''
    
        data = self.data.copy()

        data['username'] = ''

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_signup_when_username_not_sent(self):
  
        '''Signup a User - Invalid :- When the username not passed'''
        data = self.data.copy()
        data.pop('username')
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)

    def test_signup_user_when_password_empty(self):

        '''Signup a User - Invalid :- When the password is empty'''
        
        data = self.data.copy()
        data['password'] = ''
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_signup_user_when_password_not_sent(self):

        '''Signup a User - Invalid :- When the password not passed'''
    
        data = self.data.copy()
        data.pop('password')
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )

        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)

    def test_signup_user_when_first_name_empty(self):
  
        '''Signup a User - Invalid :- When the firstname is empty'''

        data = self.data.copy()
        data['first_name'] = ''

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_signup_user_when_first_name_not_sent(self):

        '''Signup a User - Invalid :- When the firstname not passed'''

        data = self.data.copy()
        data.pop('first_name')
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)
  
    def test_signup_user_when__last_name_empty(self):
  
      '''Signup a User - Invalid :- When the lastname is empty'''
  
      data = self.data.copy()
      data['last_name'] = ''

      response = self.client.post(
          reverse('accounts-create-user'),
          data
      )
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      self.assertContains(response, 'blank', status_code=400)
      self.assertContains(response, 'This field may not be blank.', status_code=400)

    def test_signup_user_when_last_name_not_sent(self):

        '''Signup a User - Invalid :- When the lastname not passed'''

        data = self.data.copy()
        data.pop('last_name')
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)
    
    def test_signup_with_existing_username(self):
        
        '''Signup a User - Invalid :- When the username already exists'''
        
        data = self.data.copy()
        data['username'] = 'tester'

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'unique', status_code=400)
        self.assertContains(response, 'This field must be unique.', status_code=400)    

    def test_signup_with_existing_email(self):

        '''Signup a User - Invalid :- When the email already exists'''

        data = self.data.copy()
        data['email'] = 'testuser@example.com'

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'unique', status_code=400)
        self.assertContains(response, 'This field must be unique.', status_code=400)   

    def test_signup_with_invalid_username(self):
        
        '''Signup a User - Invalid :- When the username is invalid type'''
        
        data = self.data.copy()
        data['username'] = 'testuser@example.com'

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Username can only contain alphanumeric characters and . or _.', status_code=400)  

    def test_signup_with_invalid_password(self):
        
        '''Signup a User - Invalid :- When the password is invalid type'''

        data = self.data.copy()
        data['password'] = 'wrongpasswordformat'

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Must have at least 1 uppercase, 1 lowercase, 1 number & 1 special character and 8 characters minimum', status_code=400)  

    def test_signup_with_invalid_email_format(self):
        
        '''Signup a User - Invalid :- When the email is invalid type'''

        data = self.data.copy()
        data['email'] = 'wrongemail'

        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Enter a valid email address.', status_code=400)  


class SignupTestValid(SignupTest):

    """
    Test class for valid signup.
    """

    @patch('apps.helpers.email_helper.send_mail')
    def test_signup_with_valid_credentials(self, send_mail):
  
        '''Signup a User - VALID :- When a valid credentials are is used to signup '''
        
        data = self.data.copy()
        response = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get('message'),
            'User Account Created Successfully.')
        self.assertContains(response, 'user', status_code=status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get('payload')['username'],
            data['username']
        )

    @patch('apps.helpers.email_helper.send_mail')
    def test_confirm_user(self, send_mail):
  
        '''Activate  and send email a User - VALID :- When a valid credentials are is used to signup '''
        
        data = self.data.copy()
        signup = self.client.post(
            reverse('accounts-create-user'),
            data
        )
        key = generate_confirmation_token(signup.data.get('payload')['email'])
        response = self.client.get(
            reverse('accounts-confirm-user',  args=[key]),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('message'),
            'User Account Activated Successfully.')
        self.assertContains(response, 'user', status_code=status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('payload')['email'],
            signup.data.get('payload')['email']
        )
        self.assertEqual(
            confirm_token(key),
            signup.data.get('payload')['email']
        )
        self.assertEquals(send_mail.call_count, 1)

        args, kwargs = send_mail.call_args_list[0]
        self.assertEquals(args[0], 'Email confirmation on Flightify')
        self.assertEquals(args[3], [signup.data.get('payload')['email']])
