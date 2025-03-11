from django import forms
from django.contrib.auth.models import User

from .models import Dish, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number", "dishes", "status"]

    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    status = forms.CharField(widget=forms.HiddenInput(), initial="waiting")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["status"].widget = forms.Select(
                choices=Order.STATUS_CHOICES
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
