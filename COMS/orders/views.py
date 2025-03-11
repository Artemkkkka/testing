from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .forms import OrderForm, UserForm
from .models import Order
from .serializers import (OrderCreateSerializer, OrderDetailSerializer,
                          OrderListSerializer, OrderStatusUpdateSerializer)


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()


class OrderDeleteAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = super().get_object()
        if obj.buyer != self.request.user:
            raise PermissionDenied("Нет прав для удаления")
        return obj


class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.buyer != self.request.user:
            raise PermissionDenied("Нет прав для изменения статуса")
        return obj


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer


def order_list(request):
    orders = Order.objects.all()
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
def add_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.buyer = request.user
        if not order.pk:
            order.status = "waiting"
        order.save()
        dishes = form.cleaned_data["dishes"]
        order.dishes.set(dishes)
        order.total_price = sum(dish.price for dish in dishes.all())
        order.save()
        return redirect("order:list")

    return render(request, "orders/create.html", {"form": form})


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(
        Order,
        pk=order_id,
    )
    if order.buyer != request.user:
        raise Http404("У вас нет прав для удаления этого заказа.")
    if request.method == "POST":
        order.delete()
        return redirect("order:list")
    context = {"form": OrderForm(instance=order), "order": order}
    return render(request, "orders/create.html", context)


@login_required
def change_status(request, order_id):
    order = get_object_or_404(
        Order,
        pk=order_id,
    )
    if order.buyer != request.user:
        raise Http404("У вас нет прав для редактирования статуса заказа.")
    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()
        return redirect("order:list")
    context = {"form": OrderForm(instance=order), "order": order}
    return render(request, "orders/create.html", context)


def search_orders(request, query):
    status_translation = dict(Order.STATUS_CHOICES)
    if query.isdigit():
        orders = Order.objects.filter(table_number__icontains=query)
    else:
        query_status = None
        for status, name in status_translation.items():
            if query == name:
                query_status = status
                break
        if query_status:
            orders = Order.objects.filter(status=query_status)
        else:
            orders = Order.objects.filter(status__icontains=query)

    return render(
        request, "orders/order_list.html", {"orders": orders, "query": query}
    )


def search_redirect(request):
    query = request.GET.get("q", "")
    if not query:
        return redirect("order:list")
    return redirect("order:search", query=query)


def calculate_revenue(request):
    paid_orders = Order.objects.filter(status="paid")
    total_revenue = sum(order.total_price for order in paid_orders)
    return render(
        request, "orders/revenue.html", {"total_revenue": total_revenue}
    )


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(
        request,
        "orders/profile.html",
        {
            "profile": user,
        },
    )


@login_required
def edit_profile(request):
    user = request.user
    form = UserForm(request.POST or None, instance=user)
    context = {"form": form}
    if form.is_valid():
        form.save()
        return redirect("order:profile", username=user.username)
    return render(request, "orders/user.html", context)
