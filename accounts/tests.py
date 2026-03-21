from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


User = get_user_model()


class RegisterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/accounts/register/'

    def test_register_user_successfully(self):
        response = self.client.post(
            self.url,
            {'username': 'newuser', 'password': 'StrongPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertNotIn('password', response.data)

        user = User.objects.get(username='newuser')
        self.assertTrue(user.check_password('StrongPass123!'))
        self.assertNotEqual(user.password, 'StrongPass123!')

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='StrongPass123!')

        response = self.client.post(
            self.url,
            {'username': 'existinguser', 'password': 'AnotherStrongPass123!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_requires_password(self):
        response = self.client.post(
            self.url,
            {'username': 'nopassword'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            self.url,
            {'username': 'weakpassuser', 'password': '12345678'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class LogoutAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='StrongPass123!')
        self.token = Token.objects.create(user=self.user)
        self.url = '/api/accounts/logout/'

    def test_logout_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out.')
        
        # Verify token is deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.user)

    def test_logout_without_authentication(self):
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token invalidtoken123')
        
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
