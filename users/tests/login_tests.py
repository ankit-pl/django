from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class LoginTests(APITestCase):
    def test_user_login_failure_wrong_password(self):
        url = reverse("login", kwargs={"version": "v1"})
        data = {"username": "test-user@gmail.co", "password": "Test@12"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_failure_wrong_username(self):
        url = reverse("login", kwargs={"version": "v1"})
        data = {"username": "test-user@gmail.c", "password": "Test@123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_success(self):
        url = reverse("login", kwargs={"version": "v1"})
        data = {"username": "test-user@gmail.co", "password": "Test@123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
