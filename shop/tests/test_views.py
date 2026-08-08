import pytest
from decimal import Decimal

from django.urls import reverse

from shop.models import Book, Category


@pytest.mark.django_db
def test_book_list_view(client):
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy",
    )

    Book.objects.create(
        title="Harry Potter",
        author="J. K. Rowling",
        description="Magic",
        price=Decimal("450.00"),
        stock=10,
        category=category,
    )

    response = client.get(reverse("book_list"))

    assert response.status_code == 200
    assert len(response.context["books"]) == 1


@pytest.mark.django_db
def test_book_detail_view(client):
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy",
    )

    book = Book.objects.create(
        title="Harry Potter",
        author="J. K. Rowling",
        description="Magic",
        price=Decimal("450.00"),
        stock=10,
        category=category,
    )

    response = client.get(reverse("book_detail", args=[book.pk]))

    assert response.status_code == 200
    assert response.context["book"] == book


@pytest.mark.django_db
def test_book_detail_404(client):
    response = client.get(reverse("book_detail", args=[999]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_search_book(client):
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy",
    )

    Book.objects.create(
        title="Harry Potter",
        author="Rowling",
        description="Magic",
        price=Decimal("100"),
        stock=5,
        category=category,
    )

    Book.objects.create(
        title="Django",
        author="Adrian",
        description="Python",
        price=Decimal("200"),
        stock=3,
        category=category,
    )

    response = client.get(reverse("book_list"), {"q": "Harry"})

    assert response.status_code == 200
    assert len(response.context["books"]) == 1
    assert response.context["books"][0].title == "Harry Potter"


@pytest.mark.django_db
def test_book_create_view_get(client):
    response = client.get(reverse("book_create"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_delete_view_get(client):
    category = Category.objects.create(
        name="Fantasy",
        slug="fantasy",
    )

    book = Book.objects.create(
        title="Delete me",
        author="Author",
        description="Test",
        price=Decimal("100"),
        stock=5,
        category=category,
    )

    response = client.get(reverse("book_delete", args=[book.pk]))

    assert response.status_code == 200
