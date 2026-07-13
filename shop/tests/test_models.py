import pytest
from decimal import Decimal

from shop.tests.factories import (
    UserFactory,
    CategoryFactory,
    BookFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_category_str():
    # Generated with AI, reviewed and modified
    category = CategoryFactory(name="Fantasy", slug="fantasy")

    assert str(category) == "Fantasy"


@pytest.mark.django_db
def test_category_repr():
    # Generated with AI, reviewed and modified
    category = CategoryFactory(name="Fantasy", slug="fantasy")

    assert repr(category) == "Fantasy"


@pytest.mark.django_db
def test_user_str():
    # Generated with AI, reviewed and modified
    user = UserFactory(username="admin")

    assert str(user) == "admin"


@pytest.mark.django_db
def test_book_str():
    # Generated with AI, reviewed and modified
    book = BookFactory(
        title="Harry Potter",
        author="J. K. Rowling",
    )

    assert str(book) == "Harry Potter (J. K. Rowling)"


@pytest.mark.django_db
def test_book_repr():
    # Generated with AI, reviewed and modified
    book = BookFactory(
        title="Harry Potter",
        author="J. K. Rowling",
    )

    assert repr(book) == "Harry Potter (J. K. Rowling)"


@pytest.mark.django_db
def test_order_str():
    # Generated with AI, reviewed and modified
    order = OrderFactory(
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@test.com",
    )

    assert str(order) == f"Order {order.id}"


@pytest.mark.django_db
def test_order_item_get_cost():
    # Generated with AI, reviewed and modified
    book = BookFactory(
        title="Harry Potter",
        author="J. K. Rowling",
        price=Decimal("450.00"),
    )

    order = OrderFactory(
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@test.com",
    )

    item = OrderItemFactory(
        order=order,
        book=book,
        price=Decimal("450.00"),
        quantity=2,
    )

    assert item.get_cost() == Decimal("900.00")


@pytest.mark.django_db
def test_order_total_cost():
    # Generated with AI, reviewed and modified
    order = OrderFactory(
        first_name="Ivan",
        last_name="Ivanov",
        email="ivan@test.com",
    )

    book1 = BookFactory(
        title="Book1",
        author="Author1",
        price=Decimal("100.00"),
    )

    book2 = BookFactory(
        title="Book2",
        author="Author2",
        price=Decimal("50.00"),
    )

    OrderItemFactory(
        order=order,
        book=book1,
        price=Decimal("100.00"),
        quantity=2,
    )

    OrderItemFactory(
        order=order,
        book=book2,
        price=Decimal("50.00"),
        quantity=3,
    )

    assert order.get_total_cost() == Decimal("350.00")


@pytest.mark.django_db
def test_user_phone_is_optional():
    # Generated with AI, reviewed and modified
    user = UserFactory(phone=None)

    assert user.phone is None


@pytest.mark.django_db
def test_book_belongs_to_category():
    # Generated with AI, reviewed and modified
    category = CategoryFactory(name="Science", slug="science")
    book = BookFactory(category=category, stock=7)

    assert book.category == category
    assert book.stock == 7


@pytest.mark.django_db
def test_order_is_created_unpaid_by_default():
    # Generated with AI, reviewed and modified
    order = OrderFactory(paid=False)

    assert order.paid is False
    assert order.stripe_session_id is None
