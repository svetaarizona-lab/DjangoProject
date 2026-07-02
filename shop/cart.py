class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def add(self, book, quantity=1):
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {"quantity": 0}

        self.cart[book_id]["quantity"] += quantity
        self.save()


    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.cart = {}
        self.session.modified = True

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def __iter__(self):
        from .models import Book

        books = Book.objects.filter(id__in=self.cart.keys())
        cart = self.cart.copy()

        for book in books:
            cart[str(book.id)]["book"] = book

        for item in cart.values():
            item["total_price"] = item["book"].price * item["quantity"]
            yield item

    def get_total_price(self):
        return sum(item["total_price"] for item in self)