import factory
from decimal import Decimal

from django.contrib.auth import get_user_model

from shop.models import Category, Book, Order, OrderItem

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "StrongPassword123"
        self.set_password(password)

        if create:
            self.save()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    category = factory.SubFactory(CategoryFactory)

    title = factory.Sequence(lambda n: f"Book {n}")
    author = "Unknown author"
    description = "Book description"
    price = Decimal("100.00")
    stock = 10


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    first_name = "John"
    last_name = "Doe"
    email = "john@test.com"
    paid = True


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)

    price = Decimal("100.00")
    quantity = 1
