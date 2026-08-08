import pytest

from shop.tests.factories import (
    UserFactory,
    CategoryFactory,
    BookFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_user_factory():
    user = UserFactory()

    assert user.username.startswith("user")
    assert user.check_password("StrongPassword123")


@pytest.mark.django_db
def test_category_factory():
    category = CategoryFactory()

    assert category.pk is not None


@pytest.mark.django_db
def test_book_factory():
    book = BookFactory()

    assert book.category is not None
    assert book.stock == 10


@pytest.mark.django_db
def test_order_factory():
    order = OrderFactory()

    assert order.paid is True


@pytest.mark.django_db
def test_order_item_factory():
    item = OrderItemFactory()

    assert item.quantity == 1
    assert item.order is not None
    assert item.book is not None
