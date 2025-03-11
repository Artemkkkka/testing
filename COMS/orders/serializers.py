from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Dish, Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(
        queryset=Dish.objects.all(), many=True
    )

    class Meta:
        model = Order
        fields = ("id", "table_number", "dishes")

    def create(self, validated_data):
        dishes_data = validated_data.pop("dishes")
        user = User.objects.get(id=2)
        if user.is_anonymous:
            raise serializers.ValidationError(
                "User must be authenticated to create an order."
            )
        order = Order.objects.create(
            buyer=user, status="waiting", **validated_data
        )
        order.dishes.set(dishes_data)
        total_price = sum(dish.price for dish in order.dishes.all())
        order.total_price = total_price
        order.save()

        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)
        read_only_fields = (
            "id", "table_number", "dishes", "total_price", "buyer"
        )


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "name", "price")


class OrderDetailSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
