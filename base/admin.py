from django.contrib import admin
from .models import Product, Order, OrderItem, BillingAddress


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "size")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "items")


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street_address")


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
