from django.urls import path
from .views import WebhookReceivedView, payment_success

urlpatterns = [
    path('webhook/', WebhookReceivedView.as_view(), name='webhook'),
    path('success/', payment_success, name='payment_success'),
]