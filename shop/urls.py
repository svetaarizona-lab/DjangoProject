from django.urls import path
from . import views
from .views import BookListView
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BookViewSet, OrderViewSet
from .views import (
    CartAPIView,
    CartAddAPIView,
    CartRemoveAPIView,
    CartClearAPIView,
)
router = DefaultRouter()

router.register(r'api/categories', CategoryViewSet)
router.register(r'api/books', BookViewSet)
router.register(r'api/orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('manage-books/', views.manage_books, name='manage_books'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('api/cart/', CartAPIView.as_view(), name='api_cart'),
    path('api/cart/add/<int:book_id>/', CartAddAPIView.as_view(), name='api_cart_add'),
    path('api/cart/remove/<int:book_id>/', CartRemoveAPIView.as_view(), name='api_cart_remove'),
    path('api/cart/clear/', CartClearAPIView.as_view(), name='api_cart_clear'),

    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('create/', views.BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('register/', views.register, name='register'),
    path('checkout/', views.CreateCheckoutSessionView.as_view(), name='checkout_session'),
    path('checkout/success/', views.payment_success, name='payment_success'),
    path('checkout/cancel/', views.payment_cancel, name='payment_cancel'),
    path("webhook/", views.stripe_webhook, name="webhook"),
    path("async/book/<int:pk>/", views.async_book, name="async_book"),
    path("async/order/<int:pk>/", views.async_order, name="async_order"),
    path("async/create-order/", views.async_create_order, name="async_create_order"),
    path("health/", views.health_check, name="health"),
]
urlpatterns += router.urls