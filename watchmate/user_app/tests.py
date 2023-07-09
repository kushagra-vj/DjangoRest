from django.contrib.auth.models import User
from django.urls import reverse

from  rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class RegistrationTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password': 'testcase@123',
            'password2': 'testcase@123'
        }
        response = self.client.post(reverse('registration'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)