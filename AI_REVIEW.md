# AI Code Review

У цьому файлі зафіксовано review трьох складних views проєкту. Рекомендації перевірені перед застосуванням.

## 1. `BookListView.get_queryset`

### Оригінальний код

```python
def get_queryset(self):
    query = self.request.GET.get("q")
    queryset = Book.objects.order_by("title")
    if query:
        queryset = queryset.filter(title__icontains=query)
    return queryset
```

### Рекомендації AI

- Залишити `icontains`, бо ORM Django параметризує запит і це не створює SQL-ін’єкцію.
- Додати docstring, щоб пояснити пошук та сортування.

### Фінальний код

```python
def get_queryset(self):
    """Return books sorted by title and optionally filtered by title."""
    query = self.request.GET.get("q")
    queryset = Book.objects.order_by("title")
    if query:
        queryset = queryset.filter(title__icontains=query)
    return queryset
```

## 2. `CreateCheckoutSessionView.post`

### Оригінальний код

```python
line_items = []
for item in cart:
    line_items.append({...})
session = stripe.checkout.Session.create(mode="payment", line_items=line_items, ...)
```

### Рекомендації AI

- Не створювати Stripe Checkout session для порожнього кошика.
- Прибрати діагностичні `print`, бо вони засмічують вивід сервера та можуть розкривати дані кошика.
- Залишити ціну, отриману з бази даних (`item["book"].price`), а не з POST-запиту.

### Фінальний код

```python
if not line_items:
    return redirect("cart_detail")

session = stripe.checkout.Session.create(
    mode="payment",
    line_items=line_items,
    customer_email=request.POST.get("email"),
    success_url=settings.DOMAIN + "/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
    cancel_url=settings.DOMAIN + "/checkout/cancel/",
)
```

## 3. `payment_success`

### Оригінальний код

```python
order = Order.objects.create(..., paid=True)
for item in cart:
    OrderItem.objects.create(order=order, ...)
    cart.clear()
send_mail(...)
```

### Рекомендації AI

- Success URL може бути відкритий повторно, тому замовлення не можна створювати без перевірки Stripe session ID.
- Додати `stripe_session_id` до Django-моделі, оскільки поле вже є у міграції.
- Очищати кошик після створення всіх позицій, а не всередині циклу.
- Надсилати email лише для щойно створеного замовлення.

### Фінальний код

```python
order, created = Order.objects.get_or_create(
    stripe_session_id=session_id,
    defaults={"first_name": "Guest", "last_name": "", "email": "", "paid": True},
)
if created:
    for item in cart:
        OrderItem.objects.create(order=order, book=item["book"], price=item["book"].price, quantity=item["quantity"])
    cart.clear()
    send_mail(...)
```

## Висновок

Застосовано лише валідні рекомендації: покращено документацію, обробку порожнього кошика та захист від дублювання замовлень. Архітектуру проєкту навмисно не змінювали.
