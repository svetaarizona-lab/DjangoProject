from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Category Slug")

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Author Name")
    bio = models.TextField(blank=True, verbose_name="Author Bio")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Author Birth Date")