from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("add/", views.add_order, name="add"),
    path("delete/<int:order_id>/", views.delete_order, name="delete"),
    path(
        "change_status/<int:order_id>/",
        views.change_status,
        name="change_status"
    ),
    path("search/<str:query>/", views.search_orders, name="search"),
    path("search-redirect/", views.search_redirect, name="search_redirect"),
    path("revenue/", views.calculate_revenue, name="calculate_revenue"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("edit/profile", views.edit_profile, name="edit_profile"),
]
