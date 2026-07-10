import pytest
from decimal import Decimal

from django.urls import reverse

from shop.models import Book
from shop.tests.factories import (
    CategoryFactory,
    BookFactory,
)


@pytest.fixture
def category():
    return CategoryFactory(
        name="History",
        slug="history",
    )


@pytest.mark.django_db
def test_create_book_flow(client, category):
    response = client.post(
        reverse("book_create"),
        {
            "category": category.id,
            "title": "Ukraine history",
            "author": "Hrushevskiy",
            "price": "500.00",
            "description": "Great book",
            "stock": 15,
        },
    )

    assert response.status_code == 302
    assert Book.objects.filter(title="Ukraine history").exists()


@pytest.mark.django_db
def test_update_book_flow(client, category):
    book = BookFactory(
        category=category,
        title="Old title",
        author="Author",
        description="Test",
        price=Decimal("100.00"),
        stock=5,
    )

    response = client.post(
        reverse("book_update", args=[book.id]),
        {
            "category": category.id,
            "title": "New title",
            "author": "Author",
            "description": "Updated",
            "price": "200.00",
            "stock": 10,
        },
    )

    assert response.status_code == 302

    book.refresh_from_db()

    assert book.title == "New title"
    assert book.price == Decimal("200.00")


@pytest.mark.django_db
def test_delete_book_flow(client, category):
    book = BookFactory(
        category=category,
        title="Delete me",
        author="Author",
    )

    response = client.post(
        reverse("book_delete", args=[book.id])
    )

    assert response.status_code == 302
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_book_search_flow(client, category):
    BookFactory(
        category=category,
        title="History",
        author="RRRR",
    )

    response = client.get(
        reverse("book_list"),
        {"q": "History"},
    )

    books = response.context["books"]

    assert response.status_code == 200
    assert len(books) == 1
    assert books[0].title == "History"