from rest_framework import serializers
from .models import Category, Book, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "price",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "created",
            "updated",
            "paid",
            "items",
        ]


class CartItemSerializer(serializers.Serializer):
    book = BookSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
