
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
stripe.api_key = settings.STRIPE_SECRET_KEY
import logging

logger = logging.getLogger(__name__)

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login,logout
from .forms import CustomUserCreationForm
from .models import Book, Order, OrderItem
from .cart import Cart
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.http import Http404

def index(request):
    return render(request,'index.html')

class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("q")

        queryset = Book.objects.order_by("title")

        if query:
            queryset = queryset.filter(title__icontains=query)

        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

class BookCreateView(CreateView):
    model = Book
    template_name = 'book_form.html'
    fields = ['category', 'title', 'author', 'price', 'description', 'stock']
    success_url = reverse_lazy('book_list')

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'book_form.html'
    fields = ['category', 'title', 'author', 'price', 'description', 'stock']
    success_url = reverse_lazy('book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book_list')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("book_list")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@permission_required("shop.can_manage_books", raise_exception=True)
def manage_books(request):
    return render(request, "manage_books.html")

def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.add(book)
    return redirect('cart_detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart_detail.html", {
        "cart": list(cart),
        "total": cart.get_total_price()
    })
class CreateCheckoutSessionView(View):
    def post(self, request):
        cart = Cart(request)

        print("SESSION CART:", request.session.get("cart"))
        print("CART OBJECT:", cart.cart)
        print("CART ITEMS:", list(cart))

        line_items = []

        for item in cart:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item["book"].title,
                    },
                    "unit_amount": int(item["book"].price * 100),
                },
                "quantity": item["quantity"],
            })
            print("LINE ITEMS:", line_items)

        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            customer_email=request.POST.get("email"),
            success_url=settings.DOMAIN + "/checkout/success/?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.DOMAIN + "/checkout/cancel/",

        )

        return redirect(session.url, code= 303)

def payment_success(request):
    session_id = request.GET.get("session_id")

    if not session_id:
        return render(request, "payment/success.html", {
            "error": "Missing session_id"
        })

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":

        cart = Cart(request)
        customer = session.customer_details

        with transaction.atomic():

            order = Order.objects.create(
                first_name=customer.get("name") if customer and customer.get("name") else "Guest",
                last_name="",
                email=customer.get("email") if customer else "",
                paid=True,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item["book"],
                    price=item["book"].price,
                    quantity=item["quantity"],
                )

                cart.clear()

        send_mail(
            subject=f"Order #{order.id}",
            message=(
                f"Thank you for your order!\n\n"
                f"Order number: {order.id}\n"
                f"Total: ${order.get_total_cost()}\n\n"
                f"We appreciate your purchase!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=False,
        )

    return render(request, "payment/success.html")

def payment_cancel(request):
    return render(request, "payment/cancel.html")
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        if not Order.objects.filter(
            stripe_session_id=session["id"]
        ).exists():

            order = Order.objects.create(
                first_name="Guest",
                last_name="",
                email=session["customer_details"]["email"],
                stripe_session_id=session["id"],
                paid=True,
            )

            print("ORDER CREATED:", order.id)

    return HttpResponse(status=200)
async def async_book(request, pk):
    try:
        book = await Book.objects.aget(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book not found")

    return render(
        request,
        "book_detail.html",
        {
            "book": book,
        },
    )


async def async_order(request, pk):
    try:
        order = await Order.objects.aget(pk=pk)
    except Order.DoesNotExist:
        raise Http404("Order not found")

    return HttpResponse(f"Order #{order.id}")


async def async_create_order(request):
    order = await Order.objects.acreate(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        paid=False,
    )

    return HttpResponse(f"Created order #{order.id}")