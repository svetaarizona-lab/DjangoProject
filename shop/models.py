
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
   # name = models.CharField(max_length=100, verbose_name="Category Name")
    #slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Book(models.Model):
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    #title = models.CharField(max_length=100, verbose_name="Book Title")
    #author = models.CharField(max_length=100, verbose_name="Book Author")
    #price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #description = models.TextField()
    #stock = models.PositiveIntegerField(default=0)
    title = models.CharField(_("Title"), max_length=255)
    author = models.CharField(_("Author"), max_length=255)
    description = models.TextField(_("Description"))
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(_("Stock"))
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title} ({self.author})'

    def __repr__(self):
        return f'{self.title} ({self.author})'

    class Meta:
        permissions = [
            ("can_add_book_stock", "Can add book stock"),
            ("can_manage_books", "Can manage books"),
            ("can_view_reports", "Can view reports"),
        ]

class Order(models.Model):
    #first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    #email = models.EmailField()

    #stripe_session_id = models.CharField(
        #max_length=255,
        #unique=True,
        #blank=True,
        #null=True,
    #)

    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    #paid = models.BooleanField(default=False)
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    paid = models.BooleanField(_("Paid"), default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    #order = models.ForeignKey(
        #Order,
        #related_name="items",
        #on_delete=models.CASCADE
    #)

    #book = models.ForeignKey(
        #Book,
        #related_name="order_items",
        #on_delete=models.CASCADE
    #)

    #price = models.DecimalField(
        #max_digits=10,
        #decimal_places=2
    #)

    #quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(
        Order,
        verbose_name=_("Order"),
        related_name="items",
        on_delete=models.CASCADE,
    )

    book = models.ForeignKey(
        Book,
        verbose_name=_("Book"),
        related_name="order_items",
        on_delete=models.CASCADE,

    )

    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(
        _("Quantity"),
        default=1,
    )

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity
    
