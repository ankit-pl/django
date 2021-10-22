from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User


class LogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test-user@gmail.co", username="Test_User", password="Test@123"
        )
        self.token = self.user.auth_token.key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_user_logout_failure_auth_token_missing(self):
        url = reverse("logout")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout_success(self):
        url = reverse("logout")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
