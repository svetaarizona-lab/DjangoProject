
from django.contrib import admin
from django.contrib.auth import views as auth_views
from shop import views
from shop.views import BookDetailView
from shop.views import BookCreateView
from shop.views import BookUpdateView
from shop.views import BookDeleteView
from django.conf import settings
from django.urls import include, path
from payments.views import WebhookReceivedView
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('admin/', admin.site.urls),

    path("i18n/setlang/", set_language, name="set_language"),

    path('', include('shop.urls')),
    path("webhook/", WebhookReceivedView.as_view(), name="webhook"),

    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('register/', views.register, name='register'),
    path("webhook/", WebhookReceivedView.as_view(), name="webhook"),

]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
]