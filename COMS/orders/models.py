from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = [
        ("waiting", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]
    table_number = models.IntegerField()
    dishes = models.ManyToManyField("Dish", related_name="orders")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="waiting"
    )
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
        related_name="orders",
    )

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number} - {self.status}"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} руб."
