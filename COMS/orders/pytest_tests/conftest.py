import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from orders.models import Dish, Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = User.objects.create_user(
        username="testuser", password="testpassword"
    )
    return user


@pytest.fixture
def order(user):
    dish1 = Dish.objects.create(name="Dish 1", price=50.00)
    dish2 = Dish.objects.create(name="Dish 2", price=50.00)
    order = Order.objects.create(
        table_number=10, buyer=user, status="waiting", total_price=100.00
    )
    order.dishes.set([dish1, dish2])

    return order
