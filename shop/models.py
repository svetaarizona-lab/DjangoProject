from django.db import models


# Create your models here.
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Book Title")
    author = models.CharField(max_length=100, verbose_name="Book Author")
    autor = models.CharField(max_length=100, verbose_name="Book Author")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Book Price")
    description = models.TextField()
    stock = models.BooleanField(default=True, verbose_name="Book Stock")
