from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import User, Order


class OrderAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="password123")

        self.client.force_authenticate(self.user)

        self.order = Order.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@test.com",
        )

    def test_get_orders(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order(self):
        response = self.client.get(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        response = self.client.post(
            "/api/orders/",
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane@test.com",
                "paid": False,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_order(self):
        response = self.client.patch(f"/api/orders/{self.order.id}/", {"paid": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(f"/api/orders/{self.order.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_own_orders(self):
        second = User.objects.create_user(username="other", password="123456")

        Order.objects.create(
            user=second,
            first_name="Other",
            last_name="User",
            email="other@test.com",
        )

        response = self.client.get("/api/orders/")

        self.assertEqual(len(response.data["results"]), 1)
