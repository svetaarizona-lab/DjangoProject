

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Book Title")
    author = models.CharField(max_length=100, verbose_name="Book Author")
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

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