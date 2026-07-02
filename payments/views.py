
import os
import json
import stripe

from django.shortcuts import redirect, render
from django.conf import settings
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail





from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
YOUR_DOMAIN = "http://127.0.0.1:8000"

stripe.api_key = settings.STRIPE_SECRET_KEY



class CheckoutPage(View):
    def get(self, request):
        return render(request, "checkout.html")



class CheckoutSession(View):
    def post(self, request):
        try:
            lookup_key = request.POST.get("lookup_key")

            if not lookup_key:
                return HttpResponse("Missing lookup_key", status=400)

            prices = stripe.Price.list(
                lookup_keys=[lookup_key],
                expand=["data.product"],
            )

            if not prices.data:
                return HttpResponse("Price not found", status=400)

            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": prices.data[0].id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=YOUR_DOMAIN + "/success/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=YOUR_DOMAIN + "/cancel/",
            )

            return redirect(session.url, code=303)

        except Exception as e:
            return HttpResponse(str(e), status=500)



class CustomerPortalView(View):
    def post(self, request):
        try:
            session_id = request.POST.get("session_id")

            if not session_id:
                return HttpResponse("Missing session_id", status=400)

            checkout_session = stripe.checkout.Session.retrieve(session_id)

            portal_session = stripe.billing_portal.Session.create(
                customer=checkout_session.customer,
                return_url=YOUR_DOMAIN + "/",
            )

            return redirect(portal_session.url, code=303)

        except Exception as e:
            return HttpResponse(str(e), status=500)



@method_decorator(csrf_exempt, name='dispatch')
class WebhookReceivedView(View):

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=settings.STRIPE_WEBHOOK_SECRET,
            )
        except Exception as e:
            return HttpResponse(str(e), status=400)

        event_type = event["type"]
        data_object = event["data"]["object"]

        print("event:", event_type)

        if event_type == "checkout.session.completed":
            if data_object.get("payment_status") == "paid":

                email = (
                    data_object.get("customer_details", {}).get("email")
                    or data_object.get("customer_email")
                )

                print("Payment succeeded!")
                print("Customer email:", email)

                if email:
                    send_mail(
                        subject="Order created",
                        message="Thank you! Your order has been created successfully.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                    )

                    print("Email sent")

        elif event_type == "customer.subscription.created":
            print("Subscription created")

        elif event_type == "customer.subscription.updated":
            print("Subscription updated")

        elif event_type == "customer.subscription.deleted":
            print("Subscription canceled")

        return JsonResponse({"status": "success"})

def payment_success(request):
    return render(request, "payment/success.html")

def payment_cancel(request):
    return render(request, "payment/cancel.html")

