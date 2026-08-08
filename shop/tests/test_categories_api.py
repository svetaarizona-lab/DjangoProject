from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import User, Category


class CategoryAPITest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="admin123"
        )

        self.client.force_authenticate(self.admin)

        self.category = Category.objects.create(name="Programming", slug="programming")

    def test_get_categories(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        response = self.client.post(
            "/api/categories/", {"name": "Python", "slug": "python"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_category(self):
        response = self.client.get(f"/api/categories/{self.category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        response = self.client.patch(
            f"/api/categories/{self.category.id}/", {"name": "Updated"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        response = self.client.delete(f"/api/categories/{self.category.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
