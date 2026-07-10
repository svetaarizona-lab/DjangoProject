import pytest
from unittest.mock import patch

from django.core.mail import send_mail


@patch("shop.views.send_mail")
def test_send_mail_mock(mock_send_mail):


    send_mail(
        subject="Test",
        message="Hello",
        from_email="admin@test.com",
        recipient_list=["user@test.com"],
    )

    mock_send_mail.assert_called_once()