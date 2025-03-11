from django.contrib import admin

from .models import Dish, Order

admin.site.register(Order)
admin.site.register(Dish)
