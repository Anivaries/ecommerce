from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from .models import Product, Order, OrderItem
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse


class ProductDetailView(DetailView):
    model = Product
    template_name = "product-detail.html"

    def get_queryset(self):
        return super().get_queryset()


class ProductListView(ListView):
    model = Product
    template_name = "products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()


def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, ordered = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    print(order_item)
    print(ordered)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect('product-detail', slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            print(f"Ima {order_item.quantity}")
            order.items.remove(order_item)
        else:
            return redirect('product-detail', slug=slug)
    else:
        return redirect('product-detail', slug=slug)
    return redirect('product-detail', slug=slug)
