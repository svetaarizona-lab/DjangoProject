import pytest

from django.contrib.auth.models import Permission
from django.urls import reverse

from shop.tests.factories import UserFactory


@pytest.mark.django_db
def test_manage_books_without_permission(client):
    user = UserFactory()

    client.force_login(user)

    response = client.get(reverse("manage_books"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_manage_books_with_permission(client):
    user = UserFactory()

    permission = Permission.objects.get(
        codename="can_manage_books"
    )

    user.user_permissions.add(permission)

    client.force_login(user)

    response = client.get(reverse("manage_books"))

    assert response.status_code == 200