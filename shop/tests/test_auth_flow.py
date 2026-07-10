
import pytest

from django.urls import reverse

from shop.models import User
from shop.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_registration_flow(client):


    response = client.post(
        reverse("register"),
        {
            "username": "john",
            "email": "john@test.com",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("login")
    assert User.objects.filter(username="john").exists()


@pytest.mark.django_db
def test_user_login_flow(client):


    UserFactory(
        username="john",
        password="StrongPassword123",
    )

    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "StrongPassword123",
        },
    )

    assert response.status_code == 302
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_user_logout_flow(client):


    user = UserFactory(
        username="john",
        password="StrongPassword123",
    )

    client.force_login(user)

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("login")
    assert "_auth_user_id" not in client.session