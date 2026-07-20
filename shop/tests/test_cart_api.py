from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import User, Category, Book


class CartAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="password123"
        )

        self.client.force_authenticate(self.user)

        self.category = Category.objects.create(
            name="Programming",
            slug="programming"
        )

        self.book = Book.objects.create(
            title="Python",
            author="Guido",
            description="Book",
            price=100,
            stock=10,
            category=self.category,
        )

    def test_get_cart(self):
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        response = self.client.post(
            f"/api/cart/add/{self.book.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_from_cart(self):
        self.client.post(f"/api/cart/add/{self.book.id}/")

        response = self.client.delete(
            f"/api/cart/remove/{self.book.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_clear_cart(self):
        self.client.post(f"/api/cart/add/{self.book.id}/")

        response = self.client.delete("/api/cart/clear/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)