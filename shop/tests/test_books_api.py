from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import User, Category, Book


class BookAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Programming", slug="programming")

        self.book = Book.objects.create(
            title="Python",
            author="Guido",
            description="Learn Python",
            price=100,
            stock=10,
            category=self.category,
        )

    def test_get_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        data = {
            "title": "Django",
            "author": "Adrian",
            "description": "DRF",
            "price": "250.00",
            "stock": 5,
            "category": self.category.id,
        }

        response = self.client.post("/api/books/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_book(self):
        response = self.client.get(f"/api/books/{self.book.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_book(self):
        response = self.client.patch(
            f"/api/books/{self.book.id}/",
            {"price": "500.00"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
