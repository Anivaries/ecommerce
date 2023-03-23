from django.contrib import admin
from .models import Product, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "size")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "items")


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
# Register your models here.
