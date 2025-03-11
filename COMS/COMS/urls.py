from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

from orders.views import (OrderCreateAPIView, OrderDeleteAPIView,
                          OrderDetailAPIView, OrderListAPIView,
                          OrderStatusUpdateAPIView)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("login"),
        ),
        name="registration",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="registration/logged_out.html"
        ),
        name="logout",
    ),
    path(
        "auth/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("api/v1/orderlist/", OrderListAPIView.as_view(), name="order-list"),
    path(
        "api/v1/orders/<int:pk>/",
        OrderDetailAPIView.as_view(),
        name="order-detail"
    ),
    path(
        "api/v1/orderlist/create/",
        OrderCreateAPIView.as_view(),
        name="order-create"
    ),
    path(
        "api/v1/orders/<int:pk>/delete/",
        OrderDeleteAPIView.as_view(),
        name="order-delete",
    ),
    path(
        "api/v1/orders/<int:pk>/status/",
        OrderStatusUpdateAPIView.as_view(),
        name="order-status-update",
    ),
    path("api/v1/auth/", include("djoser.urls")),
    path("", include("orders.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
