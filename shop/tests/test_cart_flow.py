import pytest

from django.urls import reverse

from shop.tests.factories import BookFactory


@pytest.fixture
def book():
    return BookFactory(
        title="Ukraine history",
        price="450.00",
    )


@pytest.mark.django_db
def test_add_book_to_cart(client, book):
    response = client.get(reverse("cart_add", args=[book.id]))

    assert response.status_code == 302

    session = client.session
    assert str(book.id) in session["cart"]


@pytest.mark.django_db
def test_view_cart(client, book):
    client.get(reverse("cart_add", args=[book.id]))

    response = client.get(reverse("cart_detail"))

    assert response.status_code == 200
    assert len(response.context["cart"]) == 1


@pytest.mark.django_db
def test_remove_book_from_cart(client, book):
    client.get(reverse("cart_add", args=[book.id]))
    client.get(reverse("cart_remove", args=[book.id]))

    assert str(book.id) not in client.session["cart"]


@pytest.mark.django_db
def test_clear_cart(client, book):
    client.get(reverse("cart_add", args=[book.id]))
    client.get(reverse("cart_clear"))

    assert client.session["cart"] == {}
