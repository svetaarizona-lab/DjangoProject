from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch


class PaymentFlowTest(TestCase):

    @patch("stripe.checkout.Session.retrieve")
    def test_payment_success_paid(self, mock_session):

        mock_session.return_value.payment_status = "paid"
        mock_session.return_value.customer_details = {"email": "test@test.com"}

        response = self.client.get(
            reverse("payment_success"), {"session_id": "test_session_id"}
        )

        self.assertEqual(response.status_code, 200)
