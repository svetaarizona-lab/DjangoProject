from django.db import models


# Create your models here.
from django.db import models


# Create your models here.
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
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Book Price")
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} ({self.author})'

    def __repr__(self):
        return f'{self.title} ({self.author})'

