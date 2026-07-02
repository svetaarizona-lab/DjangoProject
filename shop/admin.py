# Register your models here.
from django.contrib import admin
from .models import Category, Book

from .models import Category, Book, Order, OrderItem

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "price", "stock")
    search_fields = ("title", "author")
    list_filter = ("stock", "category")
    list_editable = ("price", "stock")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "paid",
        "created",
    )

    list_filter = (
        "paid",
        "created",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )

    inlines = [OrderItemInline]