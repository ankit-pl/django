from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User


class SignupTests(APITestCase):
    def test_user_signup_failure_password_mismatch(self):
        url = reverse("signup")
        data = {
            "email": "test-user@gmail.co",
            "username": "Test_User",
            "first_name": "Test",
            "password": "Test@123",
            "confirm_password": "Test@1234",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_failure_user_already_exists(self):
        url = reverse("signup")
        data = {
            "email": "test-user@gmail.co",
            "username": "Test_User",
            "first_name": "Test",
            "password": "Test@123",
            "confirm_password": "Test@123",
        }
        User.objects.create(
            email="test-user@gmail.co", username="Test_User", password="Test@123"
        )
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_signup_success(self):
        url = reverse("signup")
        data = {
            "email": "test-user@gmail.co",
            "username": "Test_User",
            "first_name": "Test",
            "password": "Test@123",
            "confirm_password": "Test@123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
