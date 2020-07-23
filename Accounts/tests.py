from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class SignUpTest(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(email='alexanderxchurbanov@gmail.com',
                                                  username='Test',
                                                  password='testpassword')
        self.reg_url = '/api/v1/users/'

    def test_valid_reg(self):
        data = {'email': 'alexanderx@gmail.com',
                'username': 'Test2',
                'password': 'testpassword'}
        response = self.client.post(path=self.reg_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_reg(self):
        data = {'email': self.test_user.email,
                'username': self.test_user.username,
                'password': 'testpassword'}
        response = self.client.post(path=self.reg_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.test_user_data = {'email': 'alex@gmail.com', 'password': 'testpassword'}
        self.test_user = User.objects.create_user(email=self.test_user_data['email'],
                                                  username='Test',
                                                  password=self.test_user_data['password'])
        self.jwt_login_url = '/api/v1/auth/jwt/create/'
        self.login_url = '/api/v1/auth/login/'
        self.logout_url = '/api/v1/auth/logout/'

    def test_login_logout(self):
        response = self.client.post(self.login_url, data=self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_login(self):
        response = self.client.post(self.jwt_login_url, data=self.test_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)