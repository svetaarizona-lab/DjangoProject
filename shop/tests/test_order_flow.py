import pytest
from decimal import Decimal

from shop.tests.factories import (
    BookFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_create_order_with_item():
    order = OrderFactory()

    book = BookFactory(
        price=Decimal("250.00"),
    )

    item = OrderItemFactory(
        order=order,
        book=book,
        price=Decimal("250.00"),
        quantity=2,
    )

    assert order.items.count() == 1
    assert item.get_cost() == Decimal("500.00")


@pytest.mark.django_db
def test_order_total_cost():
    order = OrderFactory()

    book = BookFactory(
        price=Decimal("250.00"),
    )

    OrderItemFactory(
        order=order,
        book=book,
        price=Decimal("250.00"),
        quantity=2,
    )

    OrderItemFactory(
        order=order,
        book=book,
        price=Decimal("250.00"),
        quantity=1,
    )

    assert order.get_total_cost() == Decimal("750.00")
