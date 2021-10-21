from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User


class CreateTransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test-user@gmail.co",
                                        username="Test_User",
                                        password="Test@123")
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token)

    def test_wallet_add_balance_failure_auth_token_missing(self):
        url = reverse('balance')
        data = {"balance": "50"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_add_balance_success(self):
        url = reverse('balance')
        data = {"balance": "50"}
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
