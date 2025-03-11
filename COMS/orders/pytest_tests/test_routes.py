import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Dish, Order


@pytest.mark.django_db
def test_order_list_view(api_client, user):
    url = reverse("order:list")
    api_client.force_authenticate(user=user)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_order_create_view(api_client, user):
    api_client.login(username=user.username, password="testpassword")
    url = reverse("order:add")
    dish1 = Dish.objects.create(name="Dish 1", price=50.00)
    dish2 = Dish.objects.create(name="Dish 2", price=100.00)
    data = {
        "table_number": "10",
        "dishes": [dish1.id, dish2.id],
        "total_price": 150.00,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_order_delete_view(api_client, user, order):
    if not order.dishes.exists():
        dish1 = Dish.objects.create(name="Dish 1", price=50.00)
        dish2 = Dish.objects.create(name="Dish 2", price=100.00)
        order.dishes.set((dish1, dish2))
    url = reverse("order:delete", args=[order.id])
    api_client.login(username=user.username, password="testpassword")
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.filter(id=order.id).exists()


@pytest.mark.django_db
def test_order_status_update_view(api_client, user, order):
    api_client.login(username=user.username, password="testpassword")
    url = reverse("order:change_status", args=(order.id,))
    data = {"status": "paid"}
    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
