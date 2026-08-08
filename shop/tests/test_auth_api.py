from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import User


class JWTAPITest(APITestCase):

    def setUp(self):
        User.objects.create_user(username="user", password="password123")

    def test_obtain_token(self):
        response = self.client.post(
            "/api/token/", {"username": "user", "password": "password123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        token = self.client.post(
            "/api/token/", {"username": "user", "password": "password123"}
        ).data

        response = self.client.post(
            "/api/token/refresh/", {"refresh": token["refresh"]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token(self):
        token = self.client.post(
            "/api/token/", {"username": "user", "password": "password123"}
        ).data

        response = self.client.post("/api/token/verify/", {"token": token["access"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_books_without_auth(self):
        self.client.force_authenticate(None)

        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_books_with_auth(self):
        user = User.objects.get(username="user")
        self.client.force_authenticate(user)

        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
