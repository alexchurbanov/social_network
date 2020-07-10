from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class SignUpTest(APITestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(email='alexanderxchurbanov@gmail.com',
                                                  username='Test',
                                                  password='testpassword')
        self.reg_url = '/users/'

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
        self.test_password = 'testpassword'
        self.test_user = User.objects.create_user(email='alexanderxchurbanov@gmail.com',
                                                  username='Test',
                                                  password=self.test_password)
        self.jwt_create_url = '/auth/jwt/create/'
        self.jwt_refresh_url = '/auth/jwt/refresh/'
        self.jwt_verify_url = '/auth/jwt/verify/'
        self.user_url = '/users/{0}/'.format(self.test_user.id)

    def test_user_update_password(self):
        data = {'email': self.test_user.email,
                'password': self.test_password}
        response = self.client.post(self.jwt_create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        jwt = response.data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(jwt['access']))
        data = {'password': 'newpassword'}
        response = self.client.patch(self.user_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'email': self.test_user.email,
                'password': self.test_password}
        response = self.client.post(self.jwt_create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)