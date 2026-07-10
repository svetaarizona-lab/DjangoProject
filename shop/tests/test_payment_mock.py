import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

from django.urls import reverse

from shop.tests.factories import BookFactory


@pytest.mark.django_db
@patch("shop.views.send_mail")
@patch("shop.views.stripe.checkout.Session.retrieve")
def test_payment_success_sends_email(
    mock_retrieve,
    mock_send_mail,
    client,
):

    customer = Mock()
    customer.name = "John Doe"
    customer.email = "john@test.com"

    session = Mock()
    session.payment_status = "paid"
    session.customer_details = customer

    mock_retrieve.return_value = session

    book = BookFactory(price=Decimal("100.00"))

    session_data = client.session
    session_data["cart"] = {
        str(book.id): {
            "quantity": 2,
        }
    }
    session_data.save()


    response = client.get(
        reverse("payment_success"),
        {
            "session_id": "cs_test_123",
        },
    )

    assert response.status_code == 200

    mock_send_mail.assert_called_once()