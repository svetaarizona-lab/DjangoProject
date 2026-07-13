from unittest.mock import patch

import shop.views as views


@patch("shop.views.send_mail")
def test_send_mail_mock(mock_send_mail):
    views.send_mail(
        subject="Test",
        message="Hello",
        from_email="admin@test.com",
        recipient_list=["user@test.com"],
    )

    mock_send_mail.assert_called_once()